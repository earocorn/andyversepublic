// https://www.developer.themoviedb.org/reference/search-movie/

// movie posters can be appended to url string http://image.tmdb.org/t/p/
import type { TMDBCredits, TMDBDetailedResponse, TMDBResponse } from '../tmdb/TMDBResponseTypes';

const optionsGET = {
	method: 'GET',
	headers: {
		accept: 'application/json',
		Authorization:
			'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3OTRjZjIzNmQ2MjMyODYwY2M0NjhmYmJkYWVmYTg2MyIsInN1YiI6IjY0YTBjNTNkNGE1MmY4MDBhZjEyMzE1YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.t8tNspVT6mQALXJCGH6GCnSaOV7464pV3PWjqOjX2zo'
	}
};

export async function getMoviesList(title: string, isAdult: boolean, isMovie: boolean): Promise<TMDBResponse | any> {
	const titleFormatted = encodeURIComponent(title);
	const media = isMovie ? 'movie' : 'tv';
	return fetch(
		`https://api.themoviedb.org/3/search/${media}?query=${titleFormatted}&include_adult=${isAdult}&language=en-US&page=1`,
		optionsGET
	)
		.then((response) => response.json())
		.then((response: (TMDBResponse)) => {
			console.info(response);
			return response;
		})
		.catch((err: any) => {
			console.error(err);
			return {
				error: err
			};
		});
}

export async function getMoreDetails(id: number, isMovie: boolean): Promise<TMDBDetailedResponse | any> {
	const media = isMovie ? 'movie' : 'tv';
	return fetch(
		`https://api.themoviedb.org/3/${media}/${id}?append_to_response=credits,similar`,
		optionsGET
	)
	.then((response) => response.json())
	.then((response: (TMDBDetailedResponse)) => {
		console.info(response);
		return response;
	})
	.catch((err: any) => {
		console.error(err);
		return {
			error: err
		}
	})
}

