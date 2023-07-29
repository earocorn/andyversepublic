
// we don't need any JS on this page, though we'll load
// it in dev so that we get hot module replacement
export const csr = true;
export const ssr = true;

// since there's no dynamic data here, we can prerender
// it so that it gets served as a static asset in production
export const prerender = true;

import type { MovieReview } from "../../server/models/MovieReview";
import { fetchPublicReviews } from "../../server/services/ReviewsHandler";

export async function load() {
    try{
    const response = await fetchPublicReviews();
    const reviews: MovieReview[] = await response.json();
    return { reviews: reviews };
    } catch(error) {
        return {'error': error};
    }
}