#!/usr/bin/env python3
"""
Script to convert knowledge base text files to PDFs
Requires: pip install reportlab
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os

def create_pdf_from_text(text_file_path, pdf_file_path, title):
    """Convert text file to PDF with proper formatting"""
    
    # Create PDF document
    doc = SimpleDocTemplate(pdf_file_path, pagesize=A4)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor='#2E86AB'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor='#A23B72'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        spaceBefore=15,
        textColor='#F18F01'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    # Add title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 20))
    
    # Read text file and process
    with open(text_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    current_section = ""
    
    for line in lines:
        line = line.strip()
        
        if not line:
            continue
            
        # Check for main sections (all caps with =)
        if line.isupper() and '=' in line:
            current_section = line.replace('=', '').strip()
            story.append(Paragraph(current_section, heading_style))
            story.append(Spacer(1, 10))
            
        # Check for subsections (numbered with .)
        elif line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.')) and '.' in line:
            subsection = line.split('.', 1)[1].strip()
            story.append(Paragraph(subsection, subheading_style))
            story.append(Spacer(1, 8))
            
        # Check for sub-subsections (numbered with .1, .2, etc.)
        elif line.startswith(('1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '3.1', '3.2', '3.3', 
                              '4.1', '4.2', '4.3', '5.1', '5.2', '5.3', '6.1', '6.2', '6.3', 
                              '7.1', '7.2', '7.3')):
            subsubsection = line.split(' ', 1)[1].strip()
            story.append(Paragraph(subsubsection, subheading_style))
            story.append(Spacer(1, 6))
            
        # Check for problem/solution patterns
        elif line.startswith('Problem:'):
            problem_text = line.replace('Problem:', '').strip()
            story.append(Paragraph(f"<b>Problem:</b> {problem_text}", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Solution:'):
            solution_text = line.replace('Solution:', '').strip()
            story.append(Paragraph(f"<b>Solution:</b> {solution_text}", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Solution Steps:'):
            story.append(Paragraph("<b>Solution Steps:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Diagnostic Steps:'):
            story.append(Paragraph("<b>Diagnostic Steps:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Resolution Steps:'):
            story.append(Paragraph("<b>Resolution Steps:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Tools Required:'):
            story.append(Paragraph("<b>Tools Required:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Resolution:'):
            story.append(Paragraph("<b>Resolution:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Required Information:'):
            story.append(Paragraph("<b>Required Information:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Verification Process:'):
            story.append(Paragraph("<b>Verification Process:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Common Updates:'):
            story.append(Paragraph("<b>Common Updates:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Access Levels:'):
            story.append(Paragraph("<b>Access Levels:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Prevention:'):
            story.append(Paragraph("<b>Prevention:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Security Features:'):
            story.append(Paragraph("<b>Security Features:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Activation Requirements:'):
            story.append(Paragraph("<b>Activation Requirements:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Plan Change Options:'):
            story.append(Paragraph("<b>Plan Change Options:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Cancellation Policies:'):
            story.append(Paragraph("<b>Cancellation Policies:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Invoice Components:'):
            story.append(Paragraph("<b>Invoice Components:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Common Discrepancies:'):
            story.append(Paragraph("<b>Common Discrepancies:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Delivery Options:'):
            story.append(Paragraph("<b>Delivery Options:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Refund Eligibility:'):
            story.append(Paragraph("<b>Refund Eligibility:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Dispute Categories:'):
            story.append(Paragraph("<b>Dispute Categories:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Chargeback Prevention:'):
            story.append(Paragraph("<b>Chargeback Prevention:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Tax Considerations:'):
            story.append(Paragraph("<b>Tax Considerations:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Tax Documents:'):
            story.append(Paragraph("<b>Tax Documents:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Compliance Areas:'):
            story.append(Paragraph("<b>Compliance Areas:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Access Levels:'):
            story.append(Paragraph("<b>Access Levels:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('API Features:'):
            story.append(Paragraph("<b>API Features:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Report Types:'):
            story.append(Paragraph("<b>Report Types:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('Tools:'):
            story.append(Paragraph("<b>Tools:</b>", body_style))
            story.append(Spacer(1, 4))
            
        elif line.startswith('MONITORING AND ALERTING'):
            story.append(Paragraph("MONITORING AND ALERTING", heading_style))
            story.append(Spacer(1, 10))
            
        elif line.startswith('PREVENTION STRATEGIES'):
            story.append(Paragraph("PREVENTION STRATEGIES", heading_style))
            story.append(Spacer(1, 10))
            
        elif line.startswith('CONTACT INFORMATION'):
            story.append(Paragraph("CONTACT INFORMATION", heading_style))
            story.append(Spacer(1, 10))
            
        elif line.startswith('SUPPORT HOURS'):
            story.append(Paragraph("SUPPORT HOURS", heading_style))
            story.append(Spacer(1, 10))
            
        elif line.startswith('BILLING SUPPORT CONTACTS'):
            story.append(Paragraph("BILLING SUPPORT CONTACTS", heading_style))
            story.append(Spacer(1, 10))
            
        elif line.startswith('TABLE OF CONTENTS'):
            story.append(Paragraph("TABLE OF CONTENTS", heading_style))
            story.append(Spacer(1, 10))
            
        # Handle numbered lists
        elif line.startswith(('1.', '2.', '3.', '4.', '5.', '6.')) and not line.startswith(('1.1', '1.2', '1.3', '2.1', '2.2', '2.3', '3.1', '3.2', '3.3', '4.1', '4.2', '4.3', '5.1', '5.2', '5.3', '6.1', '6.2', '6.3', '7.1', '7.2', '7.3')):
            list_item = line.split('.', 1)[1].strip()
            story.append(Paragraph(f"• {list_item}", body_style))
            story.append(Spacer(1, 2))
            
        # Handle dash lists
        elif line.startswith('- '):
            list_item = line[2:].strip()
            story.append(Paragraph(f"• {list_item}", body_style))
            story.append(Spacer(1, 2))
            
        # Handle regular text
        else:
            story.append(Paragraph(line, body_style))
            story.append(Spacer(1, 2))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Created PDF: {pdf_file_path}")

def main():
    """Main function to create all PDFs"""
    
    # Create knowledge_base directory if it doesn't exist
    os.makedirs('knowledge_base', exist_ok=True)
    
    # Define the knowledge base files to convert
    knowledge_files = [
        {
            'text_file': 'knowledge_base/customer_support_guide.txt',
            'pdf_file': 'knowledge_base/customer_support_guide.pdf',
            'title': 'Customer Support Knowledge Base'
        },
        {
            'text_file': 'knowledge_base/technical_troubleshooting_guide.txt',
            'pdf_file': 'knowledge_base/technical_troubleshooting_guide.pdf',
            'title': 'Technical Troubleshooting Guide'
        },
        {
            'text_file': 'knowledge_base/billing_subscription_guide.txt',
            'pdf_file': 'knowledge_base/billing_subscription_guide.pdf',
            'title': 'Billing and Subscription Guide'
        }
    ]
    
    print("🚀 Converting knowledge base files to PDFs...")
    
    for file_info in knowledge_files:
        if os.path.exists(file_info['text_file']):
            try:
                create_pdf_from_text(
                    file_info['text_file'],
                    file_info['pdf_file'],
                    file_info['title']
                )
            except Exception as e:
                print(f"❌ Error converting {file_info['text_file']}: {e}")
        else:
            print(f"⚠️  Text file not found: {file_info['text_file']}")
    
    print("\n🎉 PDF conversion complete!")
    print("📁 PDFs are now available in the knowledge_base/ directory")
    print("🤖 You can now use these PDFs with your RAG agent!")

if __name__ == "__main__":
    main()
