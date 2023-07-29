<svelte:head>
	<title>Review Manager</title>
	<meta name="description" content="Manage Reviews"/>
</svelte:head>

<script lang="ts">
	import { onMount } from "svelte";
	//@ts-ignore
	import MovieReviewTable from "../../../components/MovieReviewTable.svelte";
		
	export let data;

	$: publicReviews = data.reviews?.filter((review) => review.public === true && review.future === false);
	$: draftReviews = data.reviews?.filter((review) => review.public === false);
	$: futureReviews = data.reviews?.filter((review) => review.future === true);

	onMount(() => {

	});

</script>

<div class="container">
	<div class="container p-3">
		<div class="collapse collapse-arrow bg-base-300">
		<input type="radio" name="tables" /> 
		<div class="collapse-title text-xl font-medium">
			Public Reviews
		</div>
		<div class="collapse-content max-w-full"> 
			{#if publicReviews}
				<MovieReviewTable reviews={publicReviews}></MovieReviewTable>
			{/if}
		</div>
		</div>
		<div class="divider"></div>
		<div class="collapse collapse-arrow bg-base-300">
		<input type="radio" name="tables" /> 
		<div class="collapse-title text-xl font-medium">
			Drafts
		</div>
		<div class="collapse-content max-w-full"> 
			{#if draftReviews}
				<MovieReviewTable reviews={draftReviews}></MovieReviewTable>
			{/if}
		</div>
		</div>
		<div class="divider"></div>
		<div class="collapse collapse-arrow bg-base-300">
		<input type="radio" name="tables" /> 
		<div class="collapse-title text-xl font-medium">
			Andy's List
		</div>
		<div class="collapse-content max-w-full"> 
			{#if futureReviews}
				<MovieReviewTable reviews={futureReviews}></MovieReviewTable>
			{/if}
		</div>
		</div>
		{#if data.error}
		<div class="toast toast-center toast-middle">
			<div class="alert alert-error">
				<span>{data.error}</span>
			</div>
		</div>
		{/if}
	</div>
</div>