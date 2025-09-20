# Bonus Feature 1: Queue Worker Model with Celery and Redis

from celery import Celery
import os
from dotenv import load_dotenv
import redis

load_dotenv()

# Initialize Celery with Redis as broker and backend
celery_app = Celery(
    'financial_analyzer',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_annotations={'*': {'rate_limit': '10/s'}},
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

# Redis client for task management
redis_client = redis.Redis.from_url(os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'))

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def analyze_document_async(self, file_path: str, query: str, task_id: str):
    """
    Asynchronous task for analyzing financial documents
    
    Args:
        file_path (str): Path to the uploaded document
        query (str): User's analysis query
        task_id (str): Unique task identifier
        
    Returns:
        dict: Analysis results with status and data
    """
    try:
        # Update task status
        self.update_state(
            state='PROCESSING',
            meta={'status': 'Reading document...', 'progress': 25}
        )
        
        # Import here to avoid circular imports
        from main import run_crew
        
        # Update progress
        self.update_state(
            state='PROCESSING', 
            meta={'status': 'Analyzing with AI agents...', 'progress': 50}
        )
        
        # Run the analysis
        result = run_crew(query=query, file_path=file_path)
        
        # Update progress
        self.update_state(
            state='PROCESSING',
            meta={'status': 'Finalizing results...', 'progress': 90}
        )
        
        # Store result in Redis for retrieval
        analysis_result = {
            'status': 'success',
            'query': query,
            'analysis': str(result),
            'task_id': task_id,
            'progress': 100
        }
        
        # Cache result for 1 hour
        redis_client.setex(f'analysis_result:{task_id}', 3600, str(analysis_result))
        
        return analysis_result
        
    except Exception as exc:
        # Update task with error status
        error_result = {
            'status': 'error',
            'error': str(exc),
            'task_id': task_id
        }
        
        redis_client.setex(f'analysis_result:{task_id}', 3600, str(error_result))
        
        raise self.retry(exc=exc)

@celery_app.task
def cleanup_old_files():
    """Periodic task to cleanup old uploaded files"""
    import glob
    import time
    
    # Remove files older than 1 hour
    cutoff_time = time.time() - 3600
    
    for file_path in glob.glob('data/financial_document_*.pdf'):
        if os.path.getctime(file_path) < cutoff_time:
            try:
                os.remove(file_path)
                print(f"Cleaned up old file: {file_path}")
            except OSError:
                pass

@celery_app.task
def health_check():
    """Health check task for monitoring"""
    return {
        'status': 'healthy',
        'timestamp': str(time.time()),
        'worker_id': os.getpid()
    }

# Celery beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    'cleanup-old-files': {
        'task': 'celery_worker.cleanup_old_files',
        'schedule': 300.0,  # Run every 5 minutes
    },
    'health-check': {
        'task': 'celery_worker.health_check', 
        'schedule': 60.0,  # Run every minute
    },
}