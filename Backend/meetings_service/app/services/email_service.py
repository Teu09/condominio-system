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

    def send_meeting_invitation(self, meeting_data: dict, attendee_emails: List[str]) -> bool:
        subject = f"Convite para Reunião: {meeting_data['title']}"
        
        body = f"""
        Prezado(a) Morador(a),

        Você está convidado(a) para participar da reunião:

        Título: {meeting_data['title']}
        Data: {meeting_data['scheduled_date'].strftime('%d/%m/%Y às %H:%M')}
        Local: {meeting_data['location']}
        Organizador: {meeting_data['organizer']}

        Descrição:
        {meeting_data['description']}

        Pauta:
        {chr(10).join([f"- {item}" for item in meeting_data['agenda_items']])}

        Atenciosamente,
        Administração do Condomínio
        """

        html_body = f"""
        <html>
        <body>
            <h2>Convite para Reunião</h2>
            <p>Prezado(a) Morador(a),</p>
            <p>Você está convidado(a) para participar da reunião:</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h3>{meeting_data['title']}</h3>
                <p><strong>Data:</strong> {meeting_data['scheduled_date'].strftime('%d/%m/%Y às %H:%M')}</p>
                <p><strong>Local:</strong> {meeting_data['location']}</p>
                <p><strong>Organizador:</strong> {meeting_data['organizer']}</p>
            </div>
            
            <p><strong>Descrição:</strong></p>
            <p>{meeting_data['description']}</p>
            
            <p><strong>Pauta:</strong></p>
            <ul>
                {''.join([f'<li>{item}</li>' for item in meeting_data['agenda_items']])}
            </ul>
            
            <p>Atenciosamente,<br>Administração do Condomínio</p>
        </body>
        </html>
        """

        return self.send_email(attendee_emails, subject, body, html_body)

    def send_meeting_reminder(self, meeting_data: dict, attendee_emails: List[str]) -> bool:
        subject = f"Lembrete: Reunião {meeting_data['title']} - {meeting_data['scheduled_date'].strftime('%d/%m/%Y')}"
        
        body = f"""
        Prezado(a) Morador(a),

        Este é um lembrete sobre a reunião:

        Título: {meeting_data['title']}
        Data: {meeting_data['scheduled_date'].strftime('%d/%m/%Y às %H:%M')}
        Local: {meeting_data['location']}

        Não se esqueça de participar!

        Atenciosamente,
        Administração do Condomínio
        """

        html_body = f"""
        <html>
        <body>
            <h2>Lembrete de Reunião</h2>
            <p>Prezado(a) Morador(a),</p>
            <p>Este é um lembrete sobre a reunião:</p>
            
            <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #ffc107;">
                <h3>{meeting_data['title']}</h3>
                <p><strong>Data:</strong> {meeting_data['scheduled_date'].strftime('%d/%m/%Y às %H:%M')}</p>
                <p><strong>Local:</strong> {meeting_data['location']}</p>
            </div>
            
            <p><strong>Não se esqueça de participar!</strong></p>
            
            <p>Atenciosamente,<br>Administração do Condomínio</p>
        </body>
        </html>
        """

        return self.send_email(attendee_emails, subject, body, html_body)

    def send_meeting_minutes(self, meeting_data: dict, minutes_data: dict, attendee_emails: List[str]) -> bool:
        subject = f"Ata da Reunião: {meeting_data['title']} - {meeting_data['scheduled_date'].strftime('%d/%m/%Y')}"
        
        body = f"""
        Prezado(a) Morador(a),

        Segue em anexo a ata da reunião:

        Título: {meeting_data['title']}
        Data: {meeting_data['scheduled_date'].strftime('%d/%m/%Y às %H:%M')}
        Local: {meeting_data['location']}

        Resumo da Ata:
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
            <h2>Ata da Reunião</h2>
            <p>Prezado(a) Morador(a),</p>
            <p>Segue a ata da reunião:</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h3>{meeting_data['title']}</h3>
                <p><strong>Data:</strong> {meeting_data['scheduled_date'].strftime('%d/%m/%Y às %H:%M')}</p>
                <p><strong>Local:</strong> {meeting_data['location']}</p>
            </div>
            
            <h3>Resumo da Ata:</h3>
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

        return self.send_email(attendee_emails, subject, body, html_body)


