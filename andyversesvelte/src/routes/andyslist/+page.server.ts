import type { MovieReview } from '../../server/models/MovieReview.js';
import { fetchPublicReviews } from '../../server/services/ReviewsHandler.js';

export async function load() {
    try{
    const response = await fetchPublicReviews();
    const reviews: MovieReview[] = await response.json();
    return { reviews: reviews };
    } catch(error) {
        return {'error': error};
    }
}