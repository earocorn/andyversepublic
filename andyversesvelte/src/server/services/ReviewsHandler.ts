import { browser } from "$app/environment";
import { getTokenFromStorage } from "../authentication/authenticator";
import { API } from "../config/api";
import { auth } from "../config/firebase";
import type {MovieReview} from "../models/MovieReview";
import { currentUser } from "../stores";

export async function fetchAllMovieReviews() {
	const token = getTokenFromStorage();

	if(!token) {
		console.error('error in auth')
		return;
	}
	const url = `${API}/moviereviews/?firebase_id_token=${token}`;
	return fetch(url, {
		method: 'GET',
	});
}

export async function fetchPublicReviews() {
	const url = `${API}/moviereviews/public_reviews`;
	
	return fetch(url, {
		method: 'GET',
	});
}

export async function deleteReview(movie_id: number, firebase_id_token: string): Promise<string> {
	const url = `${API}/moviereviews/delete_by_movie_id/?movie_id=${movie_id}&firebase_id_token=${firebase_id_token}`;

	if(!auth.currentUser) {
		return 'Unauthorized';
	}

	const token = (await (auth.currentUser.getIdTokenResult())).token;
	if(token !== firebase_id_token) {
		return 'Unauthorized';
	}

	try {
		const response = await fetch(url, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
			},
		});

		if(response.ok) {
			console.info(`Review of ${movie_id} deleted succesfully.`)
			return 'success';
		} else {
			console.error('Error deleting review.');
			const errorMsg = await response.text();
			return `Error: ${errorMsg}`;
		}
	} catch (error) {
		console.error(error);
		return 'Error deleting review.'
	}
}

export async function updateReview(review: MovieReview, firebase_id_token: string): Promise<string> {
	const url = `${API}/moviereviews/update_by_movie_id/?movie_id=${review.movie_id}&firebase_id_token=${firebase_id_token}`;
	const requestBody = JSON.stringify(review);

	if(!auth.currentUser) {
		return 'Unauthorized';
	}

	const token = (await (auth.currentUser.getIdTokenResult())).token;
	if(token !== firebase_id_token || review.author_uid !== auth.currentUser.uid) {
		return 'Unauthorized';
	}

	try {
		const response = await fetch(url, {
			method: 'PATCH',
			headers: {
				'Content-Type': 'application/json',
			},
			body: requestBody,
		});

		if(response.ok) {
			console.info('Review succesfully updated');
			return 'success';
		} else {
			console.error('error updating review');
			const errorMsg = await response.text();
			return `Error: ${errorMsg}`;
		}
	} catch (error) {
		console.error(error);
		return 'Error updating review.'
	}
}

export async function postReview(review: MovieReview, firebase_id_token: string): Promise<string> {
	const url = `${API}/moviereviews/?firebase_id_token=${firebase_id_token}`;
	const requestBody = JSON.stringify(review);

	if(!auth.currentUser) {
		return 'Unauthorized';
	}

	const token = (await (auth.currentUser.getIdTokenResult())).token;
	if(token !== firebase_id_token || review.author_uid !== auth.currentUser.uid) {
		return 'Unauthorized';
	}

	try {
		const response = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: requestBody,
		});

		if(response.ok) {
			console.info(`Review of ${review.title} posted succesfully.`)
			return 'success';
		} else {
			console.error('Error posting review.');
			const errorMsg = await response.text();
			return `Error: ${errorMsg}`;
		}
	} catch (error) {
		console.error(error);
		return 'Error posting review.'
	}
}