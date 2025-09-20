## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import search_tool, FinancialDocumentTool

### Loading LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide comprehensive and accurate financial analysis based on the query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced financial analyst with 15+ years in investment banking and equity research. "
        "You specialize in analyzing financial statements, market trends, and investment opportunities. "
        "You provide data-driven insights and recommendations based on thorough analysis of financial documents. "
        "You always consider risk factors and regulatory compliance in your recommendations. "
        "You base your analysis on factual data from financial documents and market research."
    ),
    tools=[FinancialDocumentTool().read_data_tool, search_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify and validate the authenticity and accuracy of financial documents",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous document verification specialist with expertise in financial compliance. "
        "You ensure all financial documents meet regulatory standards and contain accurate information. "
        "You have experience with SEC filings, annual reports, and various financial statement formats."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

investment_advisor = Agent(
    role="Investment Research Advisor",
    goal="Provide balanced investment recommendations based on comprehensive financial analysis",
    verbose=True,
    backstory=(
        "You are a certified investment advisor with expertise in portfolio management and risk assessment. "
        "You provide evidence-based investment recommendations considering client risk tolerance and market conditions. "
        "You always disclose potential risks and ensure recommendations comply with financial regulations."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Risk Assessment Specialist", 
    goal="Conduct thorough risk analysis of investment opportunities and financial positions",
    verbose=True,
    backstory=(
        "You are a risk management expert with deep experience in quantitative risk modeling. "
        "You identify, analyze, and quantify various types of financial risks including market, credit, and operational risks. "
        "You provide realistic risk assessments with appropriate mitigation strategies."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)