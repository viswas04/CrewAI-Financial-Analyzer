## Importing libraries and files
from crewai import Task
from agents import financial_analyst
from tools import search_tool, FinancialDocumentTool

## Creating a task to analyze financial documents
analyze_financial_document = Task(
    description="""Analyze the financial document provided and address the user's query: {query}
    
    Your analysis should include:
    1. Read and understand the financial document at the provided file path
    2. Extract key financial metrics and indicators
    3. Provide insights relevant to the user's specific query
    4. Identify any notable trends, risks, or opportunities
    5. Ensure all recommendations are based on factual data from the document
    
    Use the document reading tool to access the file and search tool for additional market context if needed.""",
    
    expected_output="""A comprehensive financial analysis report including:
    - Executive summary addressing the user's query
    - Key financial metrics and ratios identified
    - Investment insights and recommendations
    - Risk factors and considerations  
    - Supporting data and evidence from the document
    - Professional conclusions with actionable recommendations
    
    Format the output as a structured report with clear sections and bullet points where appropriate.""",
    
    agent=financial_analyst,
    tools=[FinancialDocumentTool().read_data_tool, search_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="""Provide investment analysis based on the financial document data.
    
    Focus on:
    1. Revenue growth trends and sustainability
    2. Profitability metrics and margins
    3. Financial health indicators
    4. Market position and competitive advantages
    5. Future growth prospects and risks
    
    User query: {query}""",
    
    expected_output="""Investment analysis report containing:
    - Investment thesis and rationale
    - Key performance indicators analysis
    - Growth prospects evaluation
    - Risk-adjusted return expectations
    - Recommended investment strategy
    - Timeline and monitoring metrics""",
    
    agent=financial_analyst,
    tools=[FinancialDocumentTool().read_data_tool, search_tool],
    async_execution=False,
)

## Creating a risk assessment task  
risk_assessment = Task(
    description="""Conduct comprehensive risk assessment based on the financial document.
    
    Evaluate:
    1. Market risks and external factors
    2. Company-specific operational risks
    3. Financial leverage and liquidity risks
    4. Regulatory and compliance risks
    5. Industry and competitive risks
    
    Address user query: {query}""",
    
    expected_output="""Risk assessment report including:
    - Risk identification and categorization
    - Probability and impact analysis
    - Risk mitigation strategies
    - Monitoring and control recommendations
    - Overall risk rating and justification
    - Scenario analysis for different risk levels""",
    
    agent=financial_analyst,
    tools=[FinancialDocumentTool().read_data_tool, search_tool],
    async_execution=False,
)

verification_task = Task(
    description="""Verify the financial document format and content quality.
    
    Check for:
    1. Document format and readability
    2. Presence of key financial statements
    3. Data completeness and consistency
    4. Standard financial reporting elements
    
    File path: {file_path}""",
    
    expected_output="""Document verification report:
    - File format and accessibility status
    - Content structure assessment  
    - Data quality evaluation
    - Completeness score and missing elements
    - Recommendations for analysis approach""",
    
    agent=financial_analyst,
    tools=[FinancialDocumentTool().read_data_tool],
    async_execution=False
)