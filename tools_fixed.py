## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool
from crewai_tools import PDFSearchTool

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool:
    @staticmethod
    def read_data_tool(path='data/sample.pdf'):
        """Tool to read data from a pdf file from a path
        
        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.
            
        Returns:
            str: Full Financial Document content
        """
        try:
            # Use PDFSearchTool to read the PDF
            pdf_tool = PDFSearchTool(pdf=path)
            
            # Read the entire document
            full_content = ""
            
            # Try to search for common financial terms to extract content
            financial_keywords = ["revenue", "income", "financial", "balance", "cash flow", "assets", "liabilities"]
            
            for keyword in financial_keywords:
                try:
                    result = pdf_tool.run(keyword)
                    if result and result not in full_content:
                        full_content += result + "\n"
                except:
                    continue
            
            # If no content found with keywords, try to read the file directly
            if not full_content.strip():
                try:
                    with open(path, 'rb') as f:
                        import PyPDF2
                        pdf_reader = PyPDF2.PdfReader(f)
                        for page in pdf_reader.pages:
                            full_content += page.extract_text() + "\n"
                except:
                    return f"Unable to read PDF file at {path}"
            
            # Clean up the content
            while "\n\n" in full_content:
                full_content = full_content.replace("\n\n", "\n")
            
            return full_content.strip() if full_content.strip() else f"No readable content found in {path}"
            
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"

## Creating Investment Analysis Tool
class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data):
        """Analyze financial document data for investment insights"""
        if not financial_document_data or financial_document_data.strip() == "":
            return "No financial data provided for analysis"
        
        # Clean up the data format - fix the double space removal logic
        processed_data = financial_document_data
        
        # Proper way to remove double spaces
        while "  " in processed_data:  # Two spaces
            processed_data = processed_data.replace("  ", " ")
        
        # Basic analysis framework
        analysis_points = [
            "Financial data has been processed and cleaned",
            f"Document contains {len(processed_data.split())} words of financial information",
            "Recommend further detailed analysis by financial experts",
            "Investment decisions should be based on comprehensive due diligence"
        ]
        
        return "\n".join(analysis_points)

## Creating Risk Assessment Tool  
class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data):
        """Create risk assessment based on financial document data"""
        if not financial_document_data or financial_document_data.strip() == "":
            return "No financial data provided for risk assessment"
        
        risk_factors = [
            "Market risk assessment required based on document analysis",
            "Credit risk evaluation recommended",
            "Operational risk factors should be considered", 
            "Regulatory compliance risk assessment needed",
            "Liquidity risk analysis recommended"
        ]
        
        return "\n".join(risk_factors)