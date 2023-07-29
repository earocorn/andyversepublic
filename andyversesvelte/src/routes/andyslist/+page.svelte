<svelte:head>
	<title>Andy's List</title>
	<meta name="description" content="Andy's List" />
</svelte:head>

<script lang="ts">
	import "../styles/AndysList.css";
	import ContentWrapper from "../../components/ContentWrapper.svelte";
	import { onMount } from "svelte";
	import { postSuggestion } from "../../server/services/MessageHandler";
	import { invalidateAll } from "$app/navigation";

	export let data;
	$: futureReviews = data.reviews?.filter((rev) => rev.future === true)

	let suggestion = '';
	let suggestionMsg: [string, string, boolean] = ['', '', false];

	onMount(() => {
		suggestion = '';
		suggestionMsg = ['', '', false];
	})

	async function handleSubmit() {
		if(suggestion.length > 50) {
			suggestionMsg = ['warning', 'Title is too long!', false];
			await new Promise((resolve) => setTimeout(resolve, 3000));
			suggestionMsg = ['', '', false];
			return;
		}
		if(suggestion.length > 1) {
			if(suggestionMsg[0] != 'success') {
				try {
					const response = await postSuggestion(suggestion);
					if(response === 'success') {
						console.info('successfully posted message')
						suggestionMsg = [response, 'Suggestion sent! Thanks', true];
						suggestion = '';
						await new Promise((resolve) => setTimeout(resolve, 5000));
          				suggestionMsg = ['', '', false];
					} else {
						suggestionMsg = ['error', response, true]
						await new Promise((resolve) => setTimeout(resolve, 3000));
          				suggestionMsg = ['', '', false];
					}
				} catch (error) {
					console.error(error);
					suggestionMsg = ['error', 'Unknown error', false]
				}
			} 
		} else {
			suggestionMsg = ['warning', 'Please enter suggestion.', false];
		}
	}
</script>

<ContentWrapper padding={0}>
	<div class="container justify-items-stretch">
		<div class="andyslistheader text-center">
			<h1>Andy's List</h1>
				<button class="refreshbutton btn btn-ghost" on:click={() => invalidateAll()}>
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
		<div class="divider"></div>
		<h2 class="text-center font-bold">Future Reviews</h2>
		{#if data && futureReviews && futureReviews.length > 0}
			<div class="grid lg:grid-cols-3 gap-4 p-2">
				{#each futureReviews as review, i}
					<div class="card bg-base-100 shadow-xl">
						<div class="join join-vertical">
							<h3 class="text-center font-bold">{review.title}</h3>
							<figure class="card-img p-1 w-full">
								<img src={review.poster_img} alt="No poster found">
							</figure>
						</div>
					</div>
				{/each}
			</div>
		{:else}
			<h2 class="text-center">Stay tuned for Andy's future reviews!</h2>
		{/if}
		<div class="suggestionbox container grow-0 lg:w-1/4 m-auto">
			<div class="text-center bg-base-300">
				<div class="grid grid-cols-1 p-3">
					{#if suggestionMsg[0].length > 0}
					<div class="alert alert-{suggestionMsg[0]}">{suggestionMsg[1]}</div>
					{/if}
					<h4 class="font-bold">Suggest a Movie or TV Show</h4>
					<input type="text" class="input" placeholder="suggest a title" disabled={suggestionMsg[2]} bind:value={suggestion}>
					<button class="btn btn-primary" disabled={suggestionMsg[2]} on:click={handleSubmit}>Submit</button>
				</div>
			</div>
		  </div>
</ContentWrapper>