export interface TMDBMovie {
    adult: boolean
    backdrop_path: string | null;
    genre_ids: number[];
    id: number;
    original_language: string;
    original_title: string;
    overview: string;
    popularity: number;
    poster_path: string | null;
    release_date: string;
    title: string;
    video: boolean;
    vote_average: number;
    vote_count: number;
//THESE WILL BE FILLED IN IF TV SEARCH
    first_air_date: string;
    name: string;
    origin_country: string[];
}

export interface TMDBResponse {
    page: number;
    results: TMDBMovie[];
    total_pages: number;
    total_results: number;
}

export interface TMDBGenre {
    id: number;
    name: string;
}

export interface TMDBDetailedResponse {
    adult: boolean;
    backdrop_path: string | null;
    belongs_to_collection: string | null;
    budget: number;
    genres: TMDBGenre[];
    homepage: string | null;
    id: number;
    imdb_id: string | null;
    original_language: string;
    original_title: string;
    overview: string;
    popularity: number;
    poster_path: string | null;
    production_companies: { id: number; logo_path: string | null; name: string; origin_country: string }[];
    production_countries: { iso_3166_1: string; name: string }[];
    release_date: string;
    revenue: number;
    runtime: number | null;
    spoken_languages: { english_name: string; iso_639_1: string; name: string }[];
    status: string;
    tagline: string | null;
    title: string;
    video: boolean;
    vote_average: number;
    vote_count: number;
    //THESE WILL BE FILLED IN IF TV DETAILED RESPONSE
    created_by: {
        id: number;
        credit_id: string;
        name: string;
        gender: number;
        profile_path: string | null;
      }[];
      episode_run_time: number[];
      in_production: boolean;
      last_air_date: string;
      last_episode_to_air: {
        id: number;
        name: string;
        overview: string;
        air_date: string;
        episode_number: number;
        production_code: string;
        season_number: number;
        still_path: string | null;
      };
      next_episode_to_air: string | null;
      networks: {
        id: number;
        logo_path: string | null;
        name: string;
        origin_country: string;
      }[];
      number_of_episodes: number;
      number_of_seasons: number;
      origin_country: string[];
      seasons: {
        air_date: string;
        episode_count: number;
        id: number;
        name: string;
        overview: string;
        poster_path: string | null;
        season_number: number;
      }[];
    //append_to_response parameters
    credits: TMDBCredits;
    similar: TMDBResponse;
}

export interface TMDBCredits {
    id: number;
    cast: {
      adult: boolean;
      gender: number | null;
      id: number;
      known_for_department: string;
      name: string;
      original_name: string;
      popularity: number;
      profile_path: string | null;
      cast_id: number;
      character: string;
      credit_id: string;
      order: number;
    }[];
    crew: {
      adult: boolean;
      gender: number | null;
      id: number;
      known_for_department: string;
      name: string;
      original_name: string;
      popularity: number;
      profile_path: string | null;
      credit_id: string;
      department: string;
      job: string;
    }[];
  }