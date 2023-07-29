import { dev } from '$app/environment';
import type { MovieReview } from '../../../server/models/MovieReview';
import { fetchAllMovieReviews } from '../../../server/services/ReviewsHandler';

// we don't need any JS on this page, though we'll load
// it in dev so that we get hot module replacement
export const csr = dev;
export const ssr = false;

// since there's no dynamic data here, we can prerender
// it so that it gets served as a static asset in production
export const prerender = false;

export async function load() {
    try{
    const response = await fetchAllMovieReviews();
    if(response?.ok) {
        const reviews: MovieReview[] = await response.json();
        return { reviews: reviews };
    } else {
        return { 'error': 'Unauthorized!'};
    }
    } catch(error) {
        return {'error': error};
    }
}