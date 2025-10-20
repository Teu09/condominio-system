import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.from_email = settings.smtp_from_email

    def send_email(self, to_emails: List[str], subject: str, body: str, html_body: Optional[str] = None) -> bool:
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject

            # Add text body
            text_part = MIMEText(body, 'plain', 'utf-8')
            msg.attach(text_part)

            # Add HTML body if provided
            if html_body:
                html_part = MIMEText(html_body, 'html', 'utf-8')
                msg.attach(html_part)

            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)

            # Send email
            server.send_message(msg)
            server.quit()

            logger.info(f"Email sent successfully to {to_emails}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_minutes_notification(self, minutes_data: dict, recipient_emails: List[str]) -> bool:
        subject = f"Ata de Reunião: {minutes_data['title']}"
        
        body = f"""
        Prezado(a) Morador(a),

        A ata da reunião está disponível para consulta:

        Título: {minutes_data['title']}
        Data da Reunião: {minutes_data['meeting_date'].strftime('%d/%m/%Y às %H:%M')}
        Status: {minutes_data['status']}

        Resumo:
        {minutes_data['content']}

        Decisões Tomadas:
        {chr(10).join([f"- {decision}" for decision in minutes_data['decisions']])}

        Itens de Ação:
        {chr(10).join([f"- {item}" for item in minutes_data['action_items']])}

        Atenciosamente,
        Administração do Condomínio
        """

        html_body = f"""
        <html>
        <body>
            <h2>Ata de Reunião</h2>
            <p>Prezado(a) Morador(a),</p>
            <p>A ata da reunião está disponível para consulta:</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h3>{minutes_data['title']}</h3>
                <p><strong>Data da Reunião:</strong> {minutes_data['meeting_date'].strftime('%d/%m/%Y às %H:%M')}</p>
                <p><strong>Status:</strong> {minutes_data['status']}</p>
            </div>
            
            <h3>Resumo:</h3>
            <p>{minutes_data['content']}</p>
            
            <h3>Decisões Tomadas:</h3>
            <ul>
                {''.join([f'<li>{decision}</li>' for decision in minutes_data['decisions']])}
            </ul>
            
            <h3>Itens de Ação:</h3>
            <ul>
                {''.join([f'<li>{item}</li>' for item in minutes_data['action_items']])}
            </ul>
            
            <p>Atenciosamente,<br>Administração do Condomínio</p>
        </body>
        </html>
        """

        return self.send_email(recipient_emails, subject, body, html_body)

    def send_minutes_approval_request(self, minutes_data: dict, approver_emails: List[str]) -> bool:
        subject = f"Solicitação de Aprovação: Ata de Reunião - {minutes_data['title']}"
        
        body = f"""
        Prezado(a) Aprovador(a),

        Uma nova ata de reunião aguarda sua aprovação:

        Título: {minutes_data['title']}
        Data da Reunião: {minutes_data['meeting_date'].strftime('%d/%m/%Y às %H:%M')}
        Criado por: {minutes_data['created_by']}

        Resumo:
        {minutes_data['content']}

        Por favor, acesse o sistema para revisar e aprovar a ata.

        Atenciosamente,
        Sistema de Gestão Condominial
        """

        html_body = f"""
        <html>
        <body>
            <h2>Solicitação de Aprovação de Ata</h2>
            <p>Prezado(a) Aprovador(a),</p>
            <p>Uma nova ata de reunião aguarda sua aprovação:</p>
            
            <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #ffc107;">
                <h3>{minutes_data['title']}</h3>
                <p><strong>Data da Reunião:</strong> {minutes_data['meeting_date'].strftime('%d/%m/%Y às %H:%M')}</p>
                <p><strong>Criado por:</strong> {minutes_data['created_by']}</p>
            </div>
            
            <h3>Resumo:</h3>
            <p>{minutes_data['content']}</p>
            
            <p><strong>Por favor, acesse o sistema para revisar e aprovar a ata.</strong></p>
            
            <p>Atenciosamente,<br>Sistema de Gestão Condominial</p>
        </body>
        </html>
        """

        return self.send_email(approver_emails, subject, body, html_body)

    def send_minutes_rejection_notification(self, minutes_data: dict, creator_email: str, reason: str) -> bool:
        subject = f"Ata Rejeitada: {minutes_data['title']}"
        
        body = f"""
        Prezado(a) {minutes_data['created_by']},

        A ata da reunião foi rejeitada e requer correções:

        Título: {minutes_data['title']}
        Data da Reunião: {minutes_data['meeting_date'].strftime('%d/%m/%Y às %H:%M')}
        Motivo da Rejeição: {reason}

        Por favor, acesse o sistema para revisar e corrigir a ata.

        Atenciosamente,
        Sistema de Gestão Condominial
        """

        html_body = f"""
        <html>
        <body>
            <h2>Ata Rejeitada</h2>
            <p>Prezado(a) {minutes_data['created_by']},</p>
            <p>A ata da reunião foi rejeitada e requer correções:</p>
            
            <div style="background-color: #f8d7da; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #dc3545;">
                <h3>{minutes_data['title']}</h3>
                <p><strong>Data da Reunião:</strong> {minutes_data['meeting_date'].strftime('%d/%m/%Y às %H:%M')}</p>
                <p><strong>Motivo da Rejeição:</strong> {reason}</p>
            </div>
            
            <p><strong>Por favor, acesse o sistema para revisar e corrigir a ata.</strong></p>
            
            <p>Atenciosamente,<br>Sistema de Gestão Condominial</p>
        </body>
        </html>
        """

        return self.send_email([creator_email], subject, body, html_body)


