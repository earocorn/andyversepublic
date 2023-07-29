import { dev } from '$app/environment';
import type { Message } from '../../../server/models/Message';
import { fetchAllMessages } from '../../../server/services/MessageHandler';

// we don't need any JS on this page, though we'll load
// it in dev so that we get hot module replacement
export const csr = dev;
export const ssr = false;

// since there's no dynamic data here, we can prerender
// it so that it gets served as a static asset in production
export const prerender = false;

export async function load() {
    try{
    const response = await fetchAllMessages();
    if(response?.ok) {
        const messages: Message[] = await response.json();
        return { messages: messages };
    } else {
        return { 'error': 'Unauthorized!'};
    }
    } catch(error) {
        return {'error': error};
    }
}