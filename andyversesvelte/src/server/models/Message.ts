export interface Message {
    id?: string;
    sender_name: string;
    sender_email?: string;
    ip_address?: string;
    status?: string;
    message: string;
    type: 'suggestion' | 'contact';
    date_sent: string;
}