<script lang="ts">
	import { onMount } from 'svelte';
    import '../routes/styles/MovieReviewTable.css'
	import { auth } from '../server/config/firebase';
	import type { MovieReview } from "../server/models/MovieReview";
	import { deleteReview, updateReview } from '../server/services/ReviewsHandler';
	import { invalidateAll } from '$app/navigation';
    import TrashIcon from "../assets/trash.svg?raw";
    import EditIcon from "../assets/pencil.svg?raw";
		
    export let reviews: MovieReview[];

    let showDeleteModalId = 0;
    let testTitle = "";
    let editModalId = 0;
    let resultMsg = ['', ''];
    let editReview: MovieReview | null = null;

    onMount(() => {
        editReview = null;
        testTitle = "";
        showDeleteModalId = 0;
        editModalId = 0;
        resultMsg = ['', ''];
        reviews = reviews;
    });

    async function handleDelete(id: number) {
        if(id === 0) {
            return;
        }
        if(!auth.currentUser) {
            return;
        }
        try {
	    const token = (await (auth.currentUser.getIdTokenResult())).token;
            const response = await deleteReview(id, token);
            if(response === 'success') {
                invalidateAll();
                console.info('successfully deleted review');
                resultMsg = [response, 'Successfully deleted!'];
                const deletedReview = reviews.find((review) => review.id === id);
                if(deletedReview) {
                delete reviews[reviews.indexOf(deletedReview)];
                reviews = reviews;
                }
                await new Promise((resolve) => setTimeout(resolve, 5000));
                resultMsg = ['', ''];
            } else {
                resultMsg = ['error', response];
                await new Promise((resolve) => setTimeout(resolve, 3000));
                resultMsg = ['', ''];
            }
        } catch (error) {
            console.error(error);
            resultMsg = ['error', 'Unknown error'];
        }
    }

    async function handleSubmitChanges() {
        if(editReview === null) {
            return;
        }
        if(!auth.currentUser) {
            resultMsg = ['error', 'Unauthorized'];
            await new Promise((resolve) => setTimeout(resolve, 3000));
            resultMsg = ['', ''];
            return;
        }
        try {
            const token = (await (auth.currentUser.getIdTokenResult())).token;
            const response = await updateReview(editReview, token);
            if(response === 'success') {
                invalidateAll();
                console.info('updated review');
                resultMsg = [response, 'Successfully updated review!'];
                await new Promise((resolve) => setTimeout(resolve, 5000));
                resultMsg = ['', ''];
            } else {
                resultMsg = ['error', response];
                await new Promise((resolve) => setTimeout(resolve, 3000));
                resultMsg = ['', ''];
            }
        } catch (error) {
            console.error(error);
            resultMsg = ['error', 'Unknown error'];
        }
        editReview = null;
    }

</script>

<div class="container overflow-x-auto">
    <table class="table table-zebra">
        <thead>
            <tr>
                <th class="title-col">Title</th>
                <th class="media-type-col">Movie/TV</th>
                <th class="rating-col">Rating</th>
                <th class="reviewed-col">Reviewed</th>
                <th class="author-col">Author</th>
                <th class="spoiler-col">Spoiler</th>
                <th class="fav-col">Favorite</th>
                <th class="public-col">Public</th>
                <th class="actions">Actions</th>
            </tr>
        </thead>
        <tbody>
            {#each reviews as review}
                 <tr>
                    <th class="title-col">{review.title}</th>
                    <th class="media-type-col">{review.is_movie ? 'Movie' : 'TV'}</th>
                    <th class="rating-col">{review.rating/2}</th>
                    <th class="reviewed-col">{new Date(review.date_time_reviewed).toDateString().slice(4)}</th>
                    <th class="author-col">{review.author_username}</th>
                    <th class="spoiler-col">{review.spoiler_warning ? 'Y' : 'N'}</th>
                    <th class="fav-col">{review.favorited ? 'Y' : 'N'}</th>
                    <th class="public-col">{review.public ? 'Y' : 'N'}</th>
                    <th class="actions">
                        <div class="join">
                            <button class="btn btn-error btn-xs join-item tooltip" data-tip="delete" on:click={() => { 
                                showDeleteModalId = review.movie_id;
                                testTitle = review.title; 
                                }}><span>{@html TrashIcon}</span></button>
                            <button class="btn btn-warning btn-xs join-item tooltip" data-tip="edit" on:click={() => {
                                editReview = review;
                                if((review.future && review.public) || (review.public === false && review.future === false) || review.public === false) {
                                    editReview.date_time_reviewed = (new Date(Date.now())).toISOString();
                                }
                            }}><span>{@html EditIcon}</span></button>
                        </div>
                    </th>
                 </tr>
                 <dialog id="submission_confirmation_modal" class="modal" open={showDeleteModalId !== 0}>
                    <form method="dialog" class="modal-box">
                      <h3 class="font-bold text-lg">Delete {testTitle}?</h3>
                      <p class="">Are you sure you would like to delete this review?</p>
                      <div class="modal-action">
                        <div class="join rounded">
                            <button class="btn btn-error join-item" on:click={() => {
                                showDeleteModalId = 0
                                }}>Cancel</button>
                            <button class="btn btn-success join-item" on:click={() => {
                            handleDelete(showDeleteModalId ?? 0);
                            showDeleteModalId = 0;
                            }}>Yes</button>
                        </div>
                      </div>
                    </form>
                </dialog>

                <dialog id="submission_confirmation_modal" class="modal" open={editReview !== null}>
                    {#if editReview}
                    <form method="dialog" class="modal-box w-full flex flex-col">
                    <h3 class="font-bold text-lg text-center">{review.title}</h3>
                    <div class="container">
                        <div class="form-control">
                            <label for="summary">Review Summary</label>
                            <input type="text" id="summary" class="input input-bordered bg-base-200" bind:value={editReview.review_summary}>
                        </div>
                        <div class="form-control">
                            <label for="review">Review Summary</label>
                            <textarea rows="10" id="review" class="input input-bordered bg-base-200" bind:value={editReview.written_review}></textarea>
                        </div>
                        <div class="form-control lg:w-1/2 mx-auto">
                            <label for="reviewrating">{editReview.rating/2} Stars</label>
                            <input type="range" min="0" max="10" bind:value={editReview.rating} step="1" class="range range-lg range-accent">
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
                        <div class="form-control join-vertical">
                            <div class="form-control join-item">
                                <label class="cursor-pointer label">
                                    <span class="label-text text-lg">Favorite?  </span>
                                    <input type="checkbox" bind:checked={editReview.favorited} class="checkbox checkbox-warning">
                                </label>
                            </div>
                            <div class="form-control join-item">
                                <label class="cursor-pointer label">
                                    <span class="label-text text-lg">Spoiler?  </span>
                                    <input type="checkbox" bind:checked={editReview.spoiler_warning} class="checkbox checkbox-error" />
                                </label>
                            </div>
                            <div class="form-control join-item">
                                <label class="cursor-pointer label">
                                    <span class="label-text text-lg">Future Review?  </span>
                                    <input type="checkbox" bind:checked={editReview.future} class="checkbox" />
                                </label>
                            </div>
                            <div class="join join-horizontal join-item m-auto">
                                    <label class="cursor-pointer label" for="draftradio">
                                        <span class="label-text">Draft</span>
                                        <input type="radio" id="draftradio" class="radio" bind:group={editReview.public} value={false} />
                                    </label>       
                                    <label class="cursor-pointer label" for="publishradio">
                                        <span class="label-text">Public</span>
                                        <input type="radio" id="publishradio" class="radio" bind:group={editReview.public} value={true}/>
                                    </label>
                            </div>
                        </div>
                    <div class="modal-action">
                        <div class="alert alert-warning">This review will be <strong>{editReview.public ? 'PUBLIC' : 'PRIVATE'}{editReview.public ? (editReview.future ? '(Andy\'s List)' : '(Home Page)') : ''}</strong></div>
                        <div class="join rounded">
                            <button class="btn btn-error join-item" on:click={() => {
                                editReview = null;
                                }}>Cancel</button>
                            <button class="btn btn-success join-item" on:click={() => {
                                handleSubmitChanges();
                            }}>Submit</button>
                        </div>
                    </div>
                    </form>
               {/if}
                </dialog>

                {#if resultMsg[0].length > 1}
                <div class="toast toast-center toast-middle">
                    <div class="alert alert-{resultMsg[0]}">
                        <span>{resultMsg[1]}</span>
                    </div>
                </div>
                {/if}
            {/each}
        </tbody>
    </table>
    
</div>

