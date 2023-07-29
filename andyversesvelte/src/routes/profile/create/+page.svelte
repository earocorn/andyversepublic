<svelte:head>
	<title>Create</title>
	<meta name="description" content="Create Reviews"/>
</svelte:head>

<script lang="ts">
	import { onMount } from "svelte";
	import { getMoreDetails, getMoviesList } from "../../../server/services/TMDBQueries";
	import type { TMDBDetailedResponse, TMDBResponse } from "../../../server/tmdb/TMDBResponseTypes";
    import "../../styles/Create.css";
	import { browser } from "$app/environment";
	import type {MovieReview} from "../../../server/models/MovieReview";
	import { auth } from "../../../server/config/firebase";
	import { postReview } from "../../../server/services/ReviewsHandler";
	import { currentUser } from "../../../server/stores";
	import type AndyVerseUser from "../../../server/models/AndyVerseUser";
	import { goto } from "$app/navigation";

    let fetchedData: TMDBResponse | null | undefined = null;
	let movieSearch = '';
    let searchCategory = 'Movie';
    let isMovie = true;
    let fullDetails: [showFullOverview: boolean, details: TMDBDetailedResponse | null][] = [[false, null]];
    let reviewMovieId = 0;
    let newMovieReview: MovieReview | null = null;
    let backDrop: string | null = null;
    let errorMsg = "";
    let submissionConfirmation = false;
    let showSubmissionConfirmationModal = false;
    let reviewerUser: AndyVerseUser | null = null;

    let createMovieMsg = ['', ''];
    let addToListMsg = ['', ''];

    onMount(async () => {
        currentUser.subscribe((val) => {
            reviewerUser = val;
        })
        showSubmissionConfirmationModal = false;
        submissionConfirmation = false;
        errorMsg = "";
        newMovieReview = null;
        backDrop = null;
        reviewMovieId = 0;
        fetchedData = null;
        movieSearch = '';
        fullDetails = [[false, null]];
        addToListMsg = ['', ''];
        createMovieMsg = ['', ''];
    });

    async function retrieveMovie() {
        refreshDetails();
        top();
		fetchedData = null;
        fullDetails = [];
        if(searchCategory === 'Movie') {
            isMovie = true;
        } else {
            isMovie = false;
        }
		try {
			fetchedData = await getMoviesList(movieSearch, false, isMovie);
			console.log(`fetched data: ${JSON.stringify(fetchedData)}`);
            refreshDetails();
		} catch (error) {
			console.error(error);
		}
	}

    function toggleOverviewLength(index: number) {
        fullDetails[index][0] = !fullDetails[index][0];
    }

    async function showFullDescription(index: number, id: number) {
        if(!fullDetails[index][1]) {
            fullDetails[index][1] = await getMoreDetails(id, isMovie);
        }
    }

    function searchWithKey(event: KeyboardEvent) {
        if(event.key === 'Enter') {
            retrieveMovie();
        }
    }

    function refreshDetails() {
        submissionConfirmation = false;
        addToListMsg = ['', ''];
        createMovieMsg = ['', ''];
        errorMsg = "";
        backDrop = null;
        newMovieReview = null;
        reviewMovieId = 0;
        fullDetails = [];
        if(fetchedData && fetchedData.results) {
            for (let i = 0; i < fetchedData.results.length; i++) {
                fullDetails[i] = [false, null];
            }
        }
    }

    function top() {
        showSubmissionConfirmationModal = false;
        submissionConfirmation = false;
        errorMsg = "";
        if(browser) {
            refreshDetails();
            window.scrollTo({
                top: 0,
                behavior: 'smooth',
            })
        }
    }

    function chooseMovie(id: number) {
        if(fetchedData && fetchedData.results) {
            const movie = fetchedData.results.find((value) => value.id === id);
            if(movie) {
                if(auth.currentUser && reviewerUser) {
                    top();
                    backDrop = movie.backdrop_path;
                    newMovieReview = {
                        movie_id: id,
                        title: movie.title ?? movie.name,
                        poster_img: `http://image.tmdb.org/t/p/w300${movie.poster_path}` ?? '',
                        rating: 0,
                        written_review: "",
                        review_summary: "",
                        author_uid: auth.currentUser?.uid,
                        author_username: reviewerUser.username ?? auth.currentUser?.email,
                        spoiler_warning: false,
                        release_date: (new Date(movie.release_date || movie.first_air_date)).toISOString().split('T')[0],
                        date_time_reviewed: (new Date(Date.now())).toISOString(),
                        favorited: false,
                        future: false,
                        public: false,
                        is_movie: isMovie,
                    };
                    reviewMovieId = id;
                }
            }
        }
    }

    async function addToList(id: number) {
        if(fetchedData && fetchedData.results) {
            const movie = fetchedData.results.find((value) => value.id === id);
            if(movie) {
                if(auth.currentUser && reviewerUser) {
                    const reviewLater: MovieReview = {
						movie_id: movie.id,
						title: movie.title ?? movie.name,
						poster_img: `http://image.tmdb.org/t/p/w300${movie.poster_path}` ?? '',
						rating: 0,
						written_review: "FUTURE",
						review_summary: "FUTURE",
						author_uid: auth.currentUser?.uid,
                        author_username: reviewerUser.username ?? auth.currentUser?.email,
						spoiler_warning: false,
						release_date: (new Date(movie.release_date || movie.first_air_date)).toISOString().split('T')[0],
						date_time_reviewed: (new Date(Date.now())).toISOString(),
						favorited: false,
						future: true,
						public: true,
						is_movie: isMovie,
					};
                    if(auth.currentUser) {
                        const token = (await (auth.currentUser.getIdTokenResult())).token;
                        try {
                            const response = await postReview(reviewLater, token);
                            if(response === 'success') {
                                addToListMsg = [response, 'Successfully added to list!'];
						        await new Promise((resolve) => setTimeout(resolve, 2000));
                                addToListMsg = ['', ''];
                            } else {
                                addToListMsg = ['error', response];
						        await new Promise((resolve) => setTimeout(resolve, 3000));
                                addToListMsg = ['', ''];
                            }
                        } catch (error) {
                            console.error(error);
                            addToListMsg = ['error', 'Server error'];
                            await new Promise((resolve) => setTimeout(resolve, 3000));
                            addToListMsg = ['', ''];
                        }
                    }
                }
            }
        }
    }

    async function handleSubmit() {
        if(auth.currentUser) {
            const token = (await (auth.currentUser.getIdTokenResult())).token;
            if(newMovieReview) {
                try {
                    const response = await postReview(newMovieReview, token);
                    if(response === 'success') {
                        createMovieMsg = [response, 'Successfully posted review!'];
						await new Promise((resolve) => setTimeout(resolve, 2000));
                        if(browser) {
                            goto('/home');
                        }
          				createMovieMsg = ['', ''];
                    } else {
                        createMovieMsg = ['error', response];
                    }
                } catch (error) {
                    console.error(error);
                    createMovieMsg = ['error', 'Server error'];
                }
            }
        }
    }

    function goBack() {
        reviewMovieId = 0;
        submissionConfirmation = false;
        showSubmissionConfirmationModal = false;
        newMovieReview = null;
        backDrop = null;
        fetchedData = null;
        movieSearch = '';
        fullDetails = [[false, null]];
        top();
    }

    export function formatRuntime(runtime: number | null | undefined): string {
        if(runtime) {
            if(runtime > 60) {
                const hours = runtime/60;
                const remaining_seconds = runtime%60;
                const minutes = remaining_seconds;
                return `${Math.floor(hours)}h${minutes}m`;
            }
            return runtime.toString();
        }
        return '';
    }
</script>

{#if reviewMovieId === 0} 
<div class="container p-2">
    <div class="join flex-wrap">
        <input class="input input-bordered join-item bg-base-100" type="text" placeholder="Search..." on:keydown={searchWithKey} bind:value={movieSearch} />
        <select bind:value={searchCategory} on:change={retrieveMovie} class="select select-bordered input input-bordered join-item">
            <option value="Movie">Movie</option>
            <option value="TV Show">TV Show</option>
        </select>
	    <button class="btn join-item btn-secondary" on:click={retrieveMovie}>Search</button>
    </div>
    
    <h6>{fetchedData && fetchedData.results ? fetchedData.results.length + ' ' + (searchCategory) + (fetchedData.results.length > 1 ? 's Found' : ' Found') : ''}</h6>
	{#if fetchedData && fetchedData.results && fetchedData.results.length > 0}
		<div class="container p-1">
			{#each fetchedData.results as movie}

                <div class="card card-compact card-bordered lg:card-side w-full flex-none bg-base-100 shadow-xl">
                    <figure class="card-img shrink-0 h-full"><img
						src="http://image.tmdb.org/t/p/w300{movie.poster_path}"
						alt="Poster not available."
					/></figure>
                    <div class="card-body">
                        <h4 class="card-title my-0">
                            <div class="join join-vertical lg:py-5">
                                <div class="join">
                                <span class="mr-2">
                                    {#if isMovie}
                                        {movie.title}
                                    {:else}
                                        {movie.name}
                                    {/if}
                                </span>
                                <div class="items-center my-auto">
                                    <div class="badge badge-sm badge-outline p-2">
                                    <div class="rating rating-sm rating-half">
                                        <input disabled type="radio" class="rating-hidden hidden" checked={movie.vote_average === 0}/>
                                        <input disabled type="radio" class="mask mask-star-2 mask-half-1" checked={0 < movie.vote_average && movie.vote_average <= 1}/>
                                        <input disabled type="radio" class="mask mask-star-2 mask-half-2" checked={1 < movie.vote_average && movie.vote_average <= 2}/>
                                        <input disabled type="radio" class="mask mask-star-2 mask-half-1" checked={2 < movie.vote_average && movie.vote_average <= 3}/>
                                        <input disabled type="radio" class="mask mask-star-2 mask-half-2" checked={3 < movie.vote_average && movie.vote_average <= 4}/>
                                        <input disabled type="radio" class="mask mask-star-2 mask-half-1" checked={4 < movie.vote_average && movie.vote_average <= 5}/>
                                        <input disabled type="radio" class="mask mask-star-2 mask-half-2" checked={5 < movie.vote_average && movie.vote_average <= 6}/>
                                        <input disabled type="radio" class="mask mask-star-2 mask-half-1" checked={6 < movie.vote_average && movie.vote_average <= 7}/>
                                        <input disabled type="radio" class="mask mask-star-2 mask-half-2" checked={7 < movie.vote_average && movie.vote_average <= 8}/>
                                        <input disabled type="radio" class="mask mask-star-2 mask-half-1" checked={8 < movie.vote_average && movie.vote_average <= 9}/>
                                        <input disabled type="radio" class="mask mask-star-2 mask-half-2" checked={9 <= movie.vote_average && movie.vote_average <= 10}/>
                                    </div>
                                    </div>
                                </div>
                            </div>
                            <div class="font-light text-sm join-item">{`${new Date(isMovie ? movie.release_date : movie.first_air_date).toDateString().slice(4)} (${movie.original_language})`}</div>
                            {#if fullDetails[fetchedData.results.indexOf(movie)][1]}
                                {#if fetchedData && fetchedData.results && fullDetails && fullDetails[fetchedData.results.indexOf(movie)] && movie && fullDetails[fetchedData.results.indexOf(movie)][1]?.genres}
                                <div class="flex-row space-x-1 text-sm">
                                    {formatRuntime(fullDetails[fetchedData.results.indexOf(movie)][1]?.runtime)}
                                    {!isMovie ? fullDetails[fetchedData.results.indexOf(movie)][1]?.number_of_episodes + " episodes" : ''}
                                    {#each fullDetails[fetchedData.results.indexOf(movie)][1]?.genres ?? [] as genre}
                                    <div class="badge font-light">{genre.name}</div>
                                    {/each}
                                </div>
                                {:else}
                                    <div></div>
                                {/if}
                                <div class="text-sm py-3">
                                    <div>Featuring: </div>
                                    <div class="flex-row space-x-1 font-light">
                                        {#each fullDetails[fetchedData.results.indexOf(movie)][1]?.credits.cast.slice(0, 3) ?? [] as actor, i}
                                            {actor.name ? actor.name : 'Unknown'}{i < 2 ? ', ' : ''}
                                        {/each}
                                    </div>
                                </div>
                                <button class="badge badge-info" on:click={() => {
                                    if(fetchedData && fetchedData.results && fetchedData.results.length > 1 && fullDetails && fullDetails[fetchedData.results.indexOf(movie)]) {
                                        movieSearch = movie.title ?? movie.name;
                                        fetchedData = fullDetails[fetchedData.results.indexOf(movie)][1]?.similar
                                        top();
                                    }
                                    }}>{fullDetails[fetchedData.results.indexOf(movie)][1]?.similar?.results?.length ?? 0} Like This</button>
                            {:else}
                            <button class="badge badge-info" on:click={() => {
                                if(fetchedData && fetchedData.results) {
                                showFullDescription((fetchedData.results.indexOf(movie)), movie.id);
                                }
                            }}>More Details</button>
                            {/if}
                            
                            <div class="divider"/>
                            </div>
                            
                        </h4>
                        <p class="text-sm my-0 flex-grow flex-nowrap">
                            {#if fullDetails[fetchedData.results.indexOf(movie)][0] === true}
                                {movie.overview}
                            {:else}
                                {movie.overview.slice(0, 100) + '... '}
                            {/if}
                            <button class="badge badge-info" on:click={() => {
                                if(fetchedData && fetchedData.results) {
                                    toggleOverviewLength(fetchedData.results.indexOf(movie));
                                }
                            }}>{fullDetails[fetchedData.results.indexOf(movie)][0] ? 'Read Less' : 'Read More'}</button>
                        </p>
                        <div class="card-actions justify-end">
                            <button class="btn btn-outline btn-success" on:click={() => addToList(movie.id)}>Add To List</button>
                            <button class="btn btn-secondary" on:click={() => chooseMovie(movie.id)}>Review This</button>
                        </div>
                    </div>
                </div>
                <div class="divider"/>

			{/each}
		</div>
        {#if addToListMsg[0].length > 0}
    <div class="toast toast-center toast-middle">
    <div class="alert alert-{addToListMsg[0]}">
      <span>{addToListMsg[1]}</span>
    </div>
  </div>
{/if}
	{:else}
		<h4>Please search a title to get started.</h4>
	{/if}
</div>
{:else}
<div class="container rounded items-center mx-auto">
    {#if window.innerWidth < 768}
    <img src={`https://image.tmdb.org/t/p/original/${backDrop}`} alt=""/>
    {/if}
    <div class="imgcontainer aspect-video bg-contain sm:bg-repeat-none" style={window.innerWidth > 768 ? ` background-image: url('https://image.tmdb.org/t/p/original/${backDrop}');` : ""}>
    <div class="reviewcontainer rounded container overflow-none self-center lg:w-1/2 m-auto shadow-2xl bg-base-200 text-center p-2">
        {#if newMovieReview}
        <h2 class="grow-0">Review of {newMovieReview?.title}</h2>
        <div class="flex-nowrap">
            <div class="form-control">
                <label for="reviewsummary">Review Summary / Personal Title</label>
                <input bind:value={newMovieReview.review_summary} on:input={() => errorMsg = ""} type="text" id="reviewsummary" class="input input-bordered lg:w-1/4 mx-auto" placeholder="Short and sweet...">
            </div>
            <div class="form-control">
                <label for="writtenreview">Written Review</label>
                <textarea bind:value={newMovieReview.written_review} on:input={() => errorMsg = ""} id="writtenreview" cols="30" rows="10" class="textarea textarea-bordered h-36 lg:w-1/2 mx-auto" placeholder="Blah blah blah..."></textarea>
            </div>
            <div class="divider"/>
            <div class="form-control lg:w-1/2 mx-auto">
                <label for="reviewrating">{newMovieReview.rating/2} Stars</label>
                <input type="range" min="0" max="10" bind:value={newMovieReview.rating} step="1" class="range range-lg range-accent">
                <div class="rating rating-sm w-full justify-between text-xs px-2">
                    {#each Array(6) as _,i}
                        {#if i===0}
                            <input disabled type="radio" checked={false} class="mask mask-circle"/>
                        {:else}
                            <input disabled type="radio" class="mask mask-star-2"/>
                        {/if}
                        {#if (i+1 / 2) % 2 !== 0 && i < 5}
                             |
                        {/if}
                    {/each}
                </div>
            </div>
            <div class="divider"/>
            <button class="btn" on:click={() => {
                if(newMovieReview) {
                    newMovieReview.favorited = !newMovieReview.favorited
                }}}>
                Favorite
                {#if newMovieReview.favorited}
                <span class='mask mask-star mask-dashed text-yellow-400' style="font-size: x-large;">★</span>
                {:else}
                <span class='mask mask-star text-gray-400' style="font-size: x-large;">★</span>
                {/if}
            </button>
            <div class="form-control">
                <label class="cursor-pointer label mx-auto">
                    <span class="label-text text-lg">Spoiler? {newMovieReview.spoiler_warning ? 'Yes' : 'No'}</span>
                    <input type="checkbox" bind:checked={newMovieReview.spoiler_warning} class="checkbox checkbox-error" />
                  </label>
            </div>
            <div class="join join-horizontal">
                <div class="form-control mx-auto join-item">
                    <label class="cursor-pointer label" for="draftradio">
                        <span class="label-text">Draft</span>
                        <input type="radio" id="draftradio" class="radio" bind:group={newMovieReview.public} value={false} />
                    </label>
                </div>                
                <div class="form-control join-item">
                    <label class="cursor-pointer label" for="publishradio">
                        <span class="label-text">Public</span>
                        <input type="radio" id="publishradio" class="radio" bind:group={newMovieReview.public} value={true}/>
                    </label>
                </div>
            </div>
            {#if errorMsg.length > 0}
            <div class="alert alert-warning">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                <span>{errorMsg}</span>
              </div>
            {/if}
            {#if createMovieMsg[0].length > 0}
                <div class="alert alert-{createMovieMsg[0]}">{createMovieMsg[1]}</div>
            {/if}
            <div class="join join-horizontal rounded-full w-full">
                <button class="btn btn-error w-1/2 join-item" on:click={() => {
                    goBack();
                }}>Cancel</button>
                <button class="btn btn-success w-1/2 join-item" on:click={() => {
                    if(newMovieReview) {
                        if(newMovieReview.public) {
                            if(newMovieReview.written_review.length > 0 && newMovieReview.review_summary.length > 0) {
                                showSubmissionConfirmationModal = true;
                            } else {
                                errorMsg = "Published reviews require all fields.";
                                showSubmissionConfirmationModal = false;
                            }
                        } else {
                            errorMsg = "";
                            showSubmissionConfirmationModal = true;
                        }
                    } else {
                        errorMsg = "Please fill in all fields.";
                        showSubmissionConfirmationModal = false;
                    }
                    
                }}>Submit</button>
                
            </div>
            <dialog id="submission_confirmation_modal" class="modal" open={showSubmissionConfirmationModal}>
                <form method="dialog" class="modal-box">
                  <h3 class="font-bold text-lg">Confirmation</h3>
                  <p class="">Are you sure you would like to submit this review?</p>
                  <div class="modal-action">
                    <div class="join rounded">
                        <button class="btn btn-error join-item" on:click={() => showSubmissionConfirmationModal = false}>Cancel</button>
                        <button class="btn btn-success join-item" on:click={() => handleSubmit()}>Yes</button>
                    </div>
                  </div>
                </form>
            </dialog>
        </div>
        {:else}
        <div>You did not select a movie to review.</div>
            <button class="btn btn-primary btn-wide" on:click={() => {
                goBack();
            }}>Back</button>
        {/if}
        </div>
        
    </div>
</div>
{/if}