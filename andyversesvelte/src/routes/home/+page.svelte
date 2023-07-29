<svelte:head>
	<title>Home</title>
	<meta name="description" content="Hompe Page" />
</svelte:head>

<script lang='ts'>
	import '../styles/Home.css';
	import { onMount } from 'svelte';
	import type { TMDBDetailedResponse, TMDBResponse } from '../../server/tmdb/TMDBResponseTypes';
	import { getMoreDetails } from '../../server/services/TMDBQueries';
	import { browser } from '$app/environment';
	import ContentWrapper from '../../components/ContentWrapper.svelte';
	import { fetchPublicReviews } from '../../server/services/ReviewsHandler';
	import type { MovieReview } from '../../server/models/MovieReview';
					 
	export let data;
	$: publicReviews = data.reviews?.filter((review) => review.future === false);

	let fullDetails: [showFullOverview: boolean, showFullReview: boolean, details: TMDBDetailedResponse | null, similarResults: TMDBResponse | null | undefined][] = [[false, false, null, null],];

	onMount(() => {
		refreshDetails();
	});

	async function refreshList() {
		const response = await fetchPublicReviews();
    	const reviews: MovieReview[] = await response.json();
		publicReviews = reviews.filter((review) => review.future === false);
		refreshDetails();
	}

	function refreshDetails() {
		if(data && publicReviews) {
			fullDetails = new Array(publicReviews.length).fill([false, false, null, null]);
			for (let i = 0; i < publicReviews.length; i++) {
				fullDetails[i] = [false, false, null, null];
			}
		}
	}

	function toggleOverviewLength(index: number) {
		fullDetails[index][0] = !fullDetails[index][0];
	}

	async function showFullDescription(index: number, id: number, isMovie: boolean) {
		if(!fullDetails[index][2]) {
			fullDetails[index][2] = await getMoreDetails(id, isMovie);
		}
	}

	function top() {
		//fullDetails=[];
        if(browser) {
            window.scrollTo({
                top: 0,
                behavior: 'smooth',
            })
        }
    }
	
	function formatRuntime(runtime: number | null | undefined): string {
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

{#if fullDetails.length === publicReviews?.length}
<ContentWrapper padding={0}>
    <div class="container">
		<div class="homepageheader text-center">
			<h1>Andy's Reviews</h1>
				<button class="refreshbutton btn btn-ghost"on:click={() => refreshList()}>
					<svg fill="#000000" height="25px" width="25px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
						viewBox="0 0 489.698 489.698" xml:space="preserve">
							<g>
								<g>
									<path d="M468.999,227.774c-11.4,0-20.8,8.3-20.8,19.8c-1,74.9-44.2,142.6-110.3,178.9c-99.6,54.7-216,5.6-260.6-61l62.9,13.1
										c10.4,2.1,21.8-4.2,23.9-15.6c2.1-10.4-4.2-21.8-15.6-23.9l-123.7-26c-7.2-1.7-26.1,3.5-23.9,22.9l15.6,124.8
										c1,10.4,9.4,17.7,19.8,17.7c15.5,0,21.8-11.4,20.8-22.9l-7.3-60.9c101.1,121.3,229.4,104.4,306.8,69.3
										c80.1-42.7,131.1-124.8,132.1-215.4C488.799,237.174,480.399,227.774,468.999,227.774z"/>
									<path d="M20.599,261.874c11.4,0,20.8-8.3,20.8-19.8c1-74.9,44.2-142.6,110.3-178.9c99.6-54.7,216-5.6,260.6,61l-62.9-13.1
										c-10.4-2.1-21.8,4.2-23.9,15.6c-2.1,10.4,4.2,21.8,15.6,23.9l123.8,26c7.2,1.7,26.1-3.5,23.9-22.9l-15.6-124.8
										c-1-10.4-9.4-17.7-19.8-17.7c-15.5,0-21.8,11.4-20.8,22.9l7.2,60.9c-101.1-121.2-229.4-104.4-306.8-69.2
										c-80.1,42.6-131.1,124.8-132.2,215.3C0.799,252.574,9.199,261.874,20.599,261.874z"/>
								</g>
							</g>
					</svg>
				</button>
		</div>
        {#if data && publicReviews}
            <ul>
                {#each publicReviews as review, i}
						
						<div class="reviewcard card card-bordered lg:card-side bg-base-100 m-auto w-full shadow-xl">
							<figure class="card-img lg:shrink-0 h-full">
								
								<img
								src={review.poster_img}
								alt="Poster not available."
								
							/></figure>
							<div class="card-body">
								
								
								<h4 class="card-title my-0">
									<div class="join join-vertical lg:py-5">
										<div class="join">
										<span class="mr-2" style="font-size: larger;">
											<span style="font-weight: 800;">{review.title}:</span>
											<span style="font-size: large;">"{review.review_summary}"</span>
										</span>
										<div class="items-center my-auto">
											<div class="badge badge-sm badge-outline indicator p-2 lg:p-3">
												{#if review.favorited}
												<span class="indicator-item">
													<div class="rating tooltip" data-tip="andy approved">
														<input disabled type="radio" class="mask mask-star-2 bg-accent-focus">
													</div>
												</span>	
												{/if}
											<div class="rating rating-sm rating-half">
												<input disabled type="radio" class="rating-hidden hidden" checked={review.rating === 0}/>
												<input disabled type="radio" class="mask mask-star-2 mask-half-1" checked={0 < review.rating && review.rating <= 1}/>
												<input disabled type="radio" class="mask mask-star-2 mask-half-2" checked={1 < review.rating && review.rating <= 2}/>
												<input disabled type="radio" class="mask mask-star-2 mask-half-1" checked={2 < review.rating && review.rating <= 3}/>
												<input disabled type="radio" class="mask mask-star-2 mask-half-2" checked={3 < review.rating && review.rating <= 4}/>
												<input disabled type="radio" class="mask mask-star-2 mask-half-1" checked={4 < review.rating && review.rating <= 5}/>
												<input disabled type="radio" class="mask mask-star-2 mask-half-2" checked={5 < review.rating && review.rating <= 6}/>
												<input disabled type="radio" class="mask mask-star-2 mask-half-1" checked={6 < review.rating && review.rating <= 7}/>
												<input disabled type="radio" class="mask mask-star-2 mask-half-2" checked={7 < review.rating && review.rating <= 8}/>
												<input disabled type="radio" class="mask mask-star-2 mask-half-1" checked={8 < review.rating && review.rating <= 9}/>
												<input disabled type="radio" class="mask mask-star-2 mask-half-2" checked={9 <= review.rating && review.rating <= 10}/>
											</div>
											</div>
										</div>
										
									</div>
									<div class="justify-end link">Review by: {review.author_username}</div>
									<div class="font-light text-sm join-item">{`${new Date(review.release_date).toDateString().slice(4)} (Reviewed: ${new Date(review.date_time_reviewed).toDateString().slice(4)})`}</div>
									{#if fullDetails[i] && fullDetails[i][2]}
										{#if data && publicReviews && fullDetails && fullDetails[i] && review && fullDetails[i][2]?.genres}
										<div class="flex-row space-x-1 text-sm">
											{formatRuntime(fullDetails[i][2]?.runtime)}
											{!review.is_movie ? fullDetails[i][2]?.number_of_episodes + " episodes" : ''}
											{#each fullDetails[i][2]?.genres ?? [] as genre}
											<div class="badge font-light">{genre.name}</div>
											{/each}
										</div>
										{:else}
											<div></div>
										{/if}
										<div class="text-sm py-3">
											<div>Featuring: </div>
											<div class="flex-row space-x-1 font-light">
												{#each fullDetails[i][2]?.credits.cast.slice(0, 3) ?? [] as actor, i}
													{actor.name ? actor.name : 'Unknown'}{i < 2 ? ', ' : ''}
												{/each}
											</div>
										</div>
									{:else}
									<button class="badge badge-info" on:click={() => {
										if(data && publicReviews) {
										showFullDescription(i, review.movie_id, review.is_movie);
										}
									}}>{review.is_movie ? 'Movie' : 'Show'} Details</button>
									{/if}
									
									<div class="divider"/>
									{#if review.spoiler_warning}
									<div class="badge badge-error">SPOILERS!</div>
									   {/if}
									</div>
									
									
								</h4>
								<p class="text-sm my-0 flex-row flex-grow flex-nowrap">
									{#if fullDetails[i][0] === true}
										{review.written_review}
									{:else}
									<div style="{review.spoiler_warning ? 'filter: blur(3px);' : ''}">{review.written_review.slice(0, 100) + '... '}</div>
									{/if}
									<button class="badge badge-info" on:click={() => {
										if(data && publicReviews) {
											toggleOverviewLength(i);
										}
									}}>{fullDetails[i][0] ? 'Read Less' : 'Read More'}</button>
								</p>
							</div>
							{#if publicReviews && fullDetails[i] && fullDetails[i][2]}
						<div class="similarmovies container p-6 lg:max-w-lg">
							<div class="card bg-base-200 shadow-xl">
								<div class="card-body text-center">
									<div class="similarmoviestitle card-title">{review.is_movie ? 'Movies' : 'TV'} Like This</div>
									<div class="grid gap-3 grid-cols-3 grid-rows-2">
										{#each fullDetails[i][2]?.similar?.results.slice(0, 6) ?? [] as similarContent, similarIndex}
											{#if fullDetails[i][2]}
												<div class="similarmoviebox bg-base-100 rounded shadow-xl w-full">
													<img class="shrink-0 m-auto w-92" id="title{similarIndex}" src="http://image.tmdb.org/t/p/w92{similarContent.poster_path}" alt="">
													<label for="title{similarIndex}" class="text-sm">{similarContent?.title ?? similarContent?.name}</label>
												</div>
											{/if}
										{/each}
									</div>
								</div>
							</div>
						</div>
					{/if}
						</div>

					<div class="divider"></div>
                {/each}
            </ul>
        {:else}
            {JSON.stringify(data)}
        {/if}
    </div>
</ContentWrapper>
{/if}