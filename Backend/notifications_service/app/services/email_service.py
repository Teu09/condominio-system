import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.smtp_use_tls = settings.smtp_use_tls
        self.smtp_use_ssl = settings.smtp_use_ssl

    def send_email(self, 
                   to_email: str, 
                   subject: str, 
                   html_content: str, 
                   text_content: Optional[str] = None,
                   from_name: Optional[str] = None,
                   attachments: Optional[List[str]] = None) -> bool:
        """
        Send an email with HTML and optional text content
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{from_name or 'Sistema'} <{self.smtp_username}>"
            msg['To'] = to_email

            # Add text content
            if text_content:
                text_part = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(text_part)

            # Add HTML content
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)

            # Add attachments
            if attachments:
                for attachment_path in attachments:
                    try:
                        with open(attachment_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {attachment_path.split("/")[-1]}'
                            )
                            msg.attach(part)
                    except Exception as e:
                        logger.error(f"Error attaching file {attachment_path}: {str(e)}")

            # Send email
            if self.smtp_use_ssl:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    if self.smtp_use_tls:
                        server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}")
            return False

    def send_bulk_email(self, 
                       to_emails: List[str], 
                       subject: str, 
                       html_content: str, 
                       text_content: Optional[str] = None,
                       from_name: Optional[str] = None,
                       attachments: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        Send bulk emails to multiple recipients
        """
        results = {}
        
        for email in to_emails:
            try:
                success = self.send_email(
                    to_email=email,
                    subject=subject,
                    html_content=html_content,
                    text_content=text_content,
                    from_name=from_name,
                    attachments=attachments
                )
                results[email] = success
            except Exception as e:
                logger.error(f"Error sending bulk email to {email}: {str(e)}")
                results[email] = False
        
        return results

    def send_template_email(self, 
                           to_email: str, 
                           template_type: str, 
                           template_data: Dict[str, Any],
                           from_name: Optional[str] = None) -> bool:
        """
        Send an email using a template
        """
        try:
            # Get template content
            subject, html_content, text_content = self.get_template_content(template_type, template_data)
            
            return self.send_email(
                to_email=to_email,
                subject=subject,
                html_content=html_content,
                text_content=text_content,
                from_name=from_name
            )
        except Exception as e:
            logger.error(f"Error sending template email to {to_email}: {str(e)}")
            return False

    def get_template_content(self, template_type: str, template_data: Dict[str, Any]) -> tuple[str, str, str]:
        """
        Get template content based on template type
        """
        templates = {
            "welcome": {
                "subject": "Bem-vindo ao Sistema de Condomínio",
                "html": """
                <html>
                <body>
                    <h2>Bem-vindo, {name}!</h2>
                    <p>Seu cadastro foi criado com sucesso no sistema de condomínio.</p>
                    <p>Dados de acesso:</p>
                    <ul>
                        <li>Email: {email}</li>
                        <li>Senha temporária: {password}</li>
                    </ul>
                    <p>Por favor, altere sua senha no primeiro acesso.</p>
                    <p>Atenciosamente,<br>Administração do Condomínio</p>
                </body>
                </html>
                """,
                "text": "Bem-vindo, {name}! Seu cadastro foi criado com sucesso. Email: {email}, Senha: {password}"
            },
            "password_reset": {
                "subject": "Redefinição de Senha",
                "html": """
                <html>
                <body>
                    <h2>Redefinição de Senha</h2>
                    <p>Olá, {name}!</p>
                    <p>Você solicitou a redefinição de sua senha.</p>
                    <p>Nova senha: {password}</p>
                    <p>Por favor, altere esta senha no próximo acesso.</p>
                    <p>Atenciosamente,<br>Administração do Condomínio</p>
                </body>
                </html>
                """,
                "text": "Redefinição de Senha. Olá {name}! Nova senha: {password}"
            },
            "meeting_invitation": {
                "subject": "Convite para Reunião: {meeting_title}",
                "html": """
                <html>
                <body>
                    <h2>Convite para Reunião</h2>
                    <p>Olá, {name}!</p>
                    <p>Você está convidado para a reunião:</p>
                    <ul>
                        <li><strong>Título:</strong> {meeting_title}</li>
                        <li><strong>Data:</strong> {meeting_date}</li>
                        <li><strong>Horário:</strong> {meeting_time}</li>
                        <li><strong>Local:</strong> {meeting_location}</li>
                    </ul>
                    <p>{meeting_description}</p>
                    <p>Atenciosamente,<br>Administração do Condomínio</p>
                </body>
                </html>
                """,
                "text": "Convite para Reunião: {meeting_title} em {meeting_date} às {meeting_time}"
            },
            "meeting_reminder": {
                "subject": "Lembrete: Reunião {meeting_title}",
                "html": """
                <html>
                <body>
                    <h2>Lembrete de Reunião</h2>
                    <p>Olá, {name}!</p>
                    <p>Este é um lembrete da reunião:</p>
                    <ul>
                        <li><strong>Título:</strong> {meeting_title}</li>
                        <li><strong>Data:</strong> {meeting_date}</li>
                        <li><strong>Horário:</strong> {meeting_time}</li>
                        <li><strong>Local:</strong> {meeting_location}</li>
                    </ul>
                    <p>Atenciosamente,<br>Administração do Condomínio</p>
                </body>
                </html>
                """,
                "text": "Lembrete: Reunião {meeting_title} em {meeting_date} às {meeting_time}"
            },
            "minutes_ready": {
                "subject": "Ata da Reunião {meeting_title} Disponível",
                "html": """
                <html>
                <body>
                    <h2>Ata da Reunião Disponível</h2>
                    <p>Olá, {name}!</p>
                    <p>A ata da reunião <strong>{meeting_title}</strong> está disponível para download.</p>
                    <p>Data da reunião: {meeting_date}</p>
                    <p>Clique no link abaixo para baixar a ata:</p>
                    <p><a href="{download_link}">Download da Ata</a></p>
                    <p>Atenciosamente,<br>Administração do Condomínio</p>
                </body>
                </html>
                """,
                "text": "Ata da Reunião {meeting_title} disponível. Download: {download_link}"
            },
            "visitor_arrival": {
                "subject": "Visitante Chegou: {visitor_name}",
                "html": """
                <html>
                <body>
                    <h2>Visitante Chegou</h2>
                    <p>Olá, {name}!</p>
                    <p>O visitante <strong>{visitor_name}</strong> chegou ao condomínio.</p>
                    <p>Detalhes:</p>
                    <ul>
                        <li><strong>Visitante:</strong> {visitor_name}</li>
                        <li><strong>Documento:</strong> {visitor_document}</li>
                        <li><strong>Horário:</strong> {arrival_time}</li>
                        <li><strong>Unidade:</strong> {unit}</li>
                    </ul>
                    <p>Atenciosamente,<br>Portaria</p>
                </body>
                </html>
                """,
                "text": "Visitante {visitor_name} chegou às {arrival_time} na unidade {unit}"
            },
            "notice_published": {
                "subject": "Novo Aviso: {notice_title}",
                "html": """
                <html>
                <body>
                    <h2>Novo Aviso Publicado</h2>
                    <p>Olá, {name}!</p>
                    <p>Um novo aviso foi publicado no condomínio:</p>
                    <h3>{notice_title}</h3>
                    <p>{notice_content}</p>
                    <p><strong>Prioridade:</strong> {notice_priority}</p>
                    <p><strong>Data:</strong> {notice_date}</p>
                    <p>Atenciosamente,<br>Administração do Condomínio</p>
                </body>
                </html>
                """,
                "text": "Novo Aviso: {notice_title} - {notice_content}"
            },
            "maintenance_request": {
                "subject": "Solicitação de Manutenção: {request_title}",
                "html": """
                <html>
                <body>
                    <h2>Solicitação de Manutenção</h2>
                    <p>Olá, {name}!</p>
                    <p>Sua solicitação de manutenção foi registrada:</p>
                    <ul>
                        <li><strong>Título:</strong> {request_title}</li>
                        <li><strong>Descrição:</strong> {request_description}</li>
                        <li><strong>Prioridade:</strong> {request_priority}</li>
                        <li><strong>Data:</strong> {request_date}</li>
                        <li><strong>Status:</strong> {request_status}</li>
                    </ul>
                    <p>Atenciosamente,<br>Administração do Condomínio</p>
                </body>
                </html>
                """,
                "text": "Solicitação de Manutenção: {request_title} - {request_description}"
            }
        }
        
        template = templates.get(template_type, templates["welcome"])
        
        # Replace variables in template
        subject = template["subject"].format(**template_data)
        html_content = template["html"].format(**template_data)
        text_content = template["text"].format(**template_data)
        
        return subject, html_content, text_content

    def test_connection(self) -> bool:
        """
        Test SMTP connection
        """
        try:
            if self.smtp_use_ssl:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                    server.login(self.smtp_username, self.smtp_password)
            else:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    if self.smtp_use_tls:
                        server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
            
            logger.info("SMTP connection test successful")
            return True
        except Exception as e:
            logger.error(f"SMTP connection test failed: {str(e)}")
            return False

