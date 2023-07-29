import { getTokenFromStorage } from "../authentication/authenticator";
import { API } from "../config/api";
import { auth } from "../config/firebase";
import type { Message } from "../models/Message";

const urlPOST = `${API}/messages/`

export async function fetchAllMessages() {
	const token = getTokenFromStorage();

	if(!token) {
		console.error('error in auth')
		return;
	}
	const url = `${API}/messages/?firebase_id_token=${token}`;
	return fetch(url, {
		method: 'GET',
	});
}

export async function postSuggestion(suggestion: string): Promise<string> {
    if(!suggestion.trim()) {
        return 'Please enter suggestion.'
    }
    const message: Message = {
        sender_name: (auth.currentUser ? auth.currentUser?.email ?? "Anonymous Suggestion" : "Anonymous Suggestion"),
        message: suggestion.trim(),
        type: "suggestion",
        date_sent: (new Date()).toISOString(),
    }
    const requestBody = JSON.stringify(message);
    
    try {
        const response = await fetch(urlPOST, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: requestBody,
        });

        if(response.ok) {
            return 'success';
        } else {
            return 'Error processing submission.'
        }
    } catch (error) {
        console.error(error);
        return 'Error processing submission.';
    }
}

export async function postContactMessage(message: string, email:string, sender_name: string): Promise<string> {
    if(!message || !email || !sender_name) {
        return 'Please fill in all fields.'
    }

    const newMessage: Message = {
        sender_email: email,
        sender_name: sender_name,
        message: message,
        type: "contact",
        date_sent: (new Date()).toISOString(),
    }
    const requestBody = JSON.stringify(newMessage);

    try {
        const response = await fetch(urlPOST, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: requestBody,
        });

        if(response.ok) {
            return 'success';
        } else {
            return 'Error processing submission.'
        }
    } catch (error) {
        console.error(error);
        return 'Error processing submission.';
    }
}

export async function deleteMessages(ids: string[]): Promise<string> {
    const token = getTokenFromStorage();
    if(!token) {
        return 'error in auth';
    }
    const url = `${API}/messages/delete_messages/?firebase_id_token=${token}`
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ids }),
        });
        if(response.ok) {
            return 'success';
        } else {
            return 'Unable to delete messages.';
        }
    } catch (error) {
        return 'Error deleting messages.';
    }
}

export async function markAsRead(id: string) {
    const token = getTokenFromStorage();

	if(!token) {
		console.error('error in auth')
		return;
	}
	const url = `${API}/messages/${id}/mark_read/?firebase_id_token=${token}`;
	try {
        const response = await fetch(url, {
            method: 'PATCH',
        });
        if(response.ok) {
            return 'success';
        } else {
            return 'Was unable to update message.'
        }
    } catch (error) {
        return 'Error marking message as read.';
    }
}