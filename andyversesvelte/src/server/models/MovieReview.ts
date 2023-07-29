export interface MovieReview {
	id?: number;
	movie_id: number;
	title: string;
	poster_img: string;
	rating: number;
	written_review: string;
    review_summary: string;
	author_uid: string;
	author_username: string;
	spoiler_warning: boolean;
	release_date: string;
	date_time_reviewed: string;
	favorited: boolean;
	future: boolean;
	public: boolean;
    is_movie: boolean;
}