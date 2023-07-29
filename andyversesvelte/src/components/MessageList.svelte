<script lang="ts">
	import { onMount } from 'svelte';
    import '../routes/styles/MessageList.css'
	import { auth } from '../server/config/firebase';
	import { deleteReview } from '../server/services/ReviewsHandler';
	import { invalidateAll } from '$app/navigation';
	import type { Message } from '../server/models/Message';
	import { deleteMessages, markAsRead } from '../server/services/MessageHandler';
	
    export let messages: Message[];
    export let type: 'suggestion' | 'contact';

    let selectedMessageIds: string[] = [];
    let selectAll: boolean = false;
    let showDeleteModal = false;
    let showMessageDetails: Message | null = null;
    let resultMsg = ['', ''];

    onMount(() => {
        showMessageDetails = null;
        selectedMessageIds = [];
        showDeleteModal = false;
        resultMsg = ['', ''];
        messages = messages;
    });

    async function handleDelete(ids: string[]) {
        if(ids.length === 0) {
            return;
        }
        if(!auth.currentUser) {
            return;
        }
        try {
            const response = await deleteMessages(ids)
            if(response === 'success') {
                invalidateAll();
                console.info('successfully deleted messages');
                resultMsg = [response, 'Succesfully deleted!'];
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

    function toggleSelectAll() {
        selectAll = !selectAll;
        if (selectAll) {
            selectedMessageIds = messages.map((message) => message.id ?? ' ');
        } else {
            selectedMessageIds = [];
        }
    }

    function toggleIndividual(id: string) {
        if(id === ' ') {
            return;
        }
        if(selectedMessageIds.includes(id)) {
            selectedMessageIds = selectedMessageIds.filter((messageId) => messageId !== id);
        } else {
            selectedMessageIds = [...selectedMessageIds, id];
        }
        if(selectedMessageIds.length === 0) {
            selectAll = false;
        }
    }

    function openMessage(message: Message) {
        if(message.id) {
            if(message.status === 'unread') {
                markAsRead(message.id);
                messages[messages.indexOf(message)].status = 'read';
            }
            showMessageDetails = message;
        }
    }
</script>

{#if type=='contact'}
     <!-- content here -->
<div class="container overflow-x-auto">
    <button class="btn btn-error" on:click={() => {
        if(selectedMessageIds.length > 0) {
            showDeleteModal = true;
        }
        }}>Delete Selected Messages</button>
    <table class="table table-zebra">
        <thead>
            <tr>
                <th class="checked-col"><input type="checkbox" class="checkbox bordered" bind:checked={selectAll} on:click={toggleSelectAll}></th>
                <th class="status-col">Status</th>
                <th class="date-col">Date</th>
                <th class="name-col">Name</th>
                <th class="email-col">Email</th>
                <th class="actions">Actions</th>
            </tr>
        </thead>
        <tbody>
            {#each messages as message}
                 <tr>
                    <th class="checked-col"><input type="checkbox" class="checkbox bordered" checked={selectedMessageIds.includes(message.id ?? ' ')} on:change={() => toggleIndividual(message.id ?? ' ')}></th>
                    <th class="status-col">
                        <div class="badge badge-sm badge-{message.status === 'unread' ? 'warning' : 'success'}">{message.status?.toUpperCase()}</div>
                    </th>
                    <th class="date-col text-xs">{new Date(message.date_sent).toDateString().slice(4)}</th>
                    <th class="name-col">{message.sender_name}</th>
                    <th class="email-col">{message.sender_email}</th>
                    <th class="actions">
                        <div class="join">
                            <button class="btn btn-info btn-xs join-item" on:click={() => {openMessage(message)}}>VIEW</button>
                        </div>
                    </th>
                 </tr>
                 <dialog id="viewMessage" class="modal" open={showMessageDetails !== null}>
                    <form method="dialog" class="modal-box">
                        <h3 class="font-bold text-lg">Message from: {showMessageDetails?.sender_email} ({showMessageDetails && showMessageDetails.date_sent && new Date(showMessageDetails?.date_sent).toDateString().slice(4)})</h3>
                        <h3>{showMessageDetails?.sender_name} says:</h3>
                        <p>{showMessageDetails?.message}</p>
                        <div class="modal-action">
                            <a href="mailto:{showMessageDetails?.sender_email}" class="btn link link-info">Respond to {showMessageDetails?.sender_email}</a>
                            <button class="btn" on:click={() => {showMessageDetails = null}}>Close</button>
                        </div>
                    </form>
                </dialog>
                <dialog id="submission_confirmation_modal" class="modal" open={showDeleteModal}>
                    <form method="dialog" class="modal-box">
                      <h3 class="font-bold text-lg">Deletion Confirmation</h3>
                      <p class="">Are you sure you would like to delete {selectedMessageIds.length > 1 ? 'these messages?' : 'this message?'}</p>
                      <div class="modal-action">
                        <div class="join rounded">
                            <button class="btn btn-error join-item" on:click={() => {
                                showDeleteModal = false;
                                }}>Cancel</button>
                            <button class="btn btn-success join-item" on:click={() => {
                            handleDelete(selectedMessageIds ?? ' ');
                            showDeleteModal = false;
                            }}>Yes</button>
                        </div>
                      </div>
                    </form>
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
{:else}
<div class="container overflow-x-auto">
    <button class="btn btn-error" on:click={() => {
        if(selectedMessageIds.length > 0) {
            showDeleteModal = true;
        }
        }}>Delete Selected Messages</button>
        <table class="table table-zebra">
            <thead>
                <tr>
                    <th class="checked-col"><input type="checkbox" class="checkbox bordered" bind:checked={selectAll} on:click={toggleSelectAll}></th>
                    <th class="date-col">Date</th>
                    <th class="suggestion-col">Suggestion</th>
                </tr>
            </thead>
            <tbody>
                {#each messages as message}
                     <tr>
                        <th class="checked-col"><input type="checkbox" class="checkbox bordered" checked={selectedMessageIds.includes(message.id ?? ' ')} on:change={() => toggleIndividual(message.id ?? ' ')}></th>
                        <th class="date-col text-xs">{new Date(message.date_sent).toDateString().slice(4)}</th>
                        <th class="suggestion-col">{message.message}</th>
                     </tr>
                    <dialog id="submission_confirmation_modal" class="modal" open={showDeleteModal}>
                        <form method="dialog" class="modal-box">
                          <h3 class="font-bold text-lg">Deletion Confirmation</h3>
                          <p class="">Are you sure you would like to delete {selectedMessageIds.length > 1 ? 'these messages?' : 'this message?'}</p>
                          <div class="modal-action">
                            <div class="join rounded">
                                <button class="btn btn-error join-item" on:click={() => {
                                    showDeleteModal = false;
                                    }}>Cancel</button>
                                <button class="btn btn-success join-item" on:click={() => {
                                handleDelete(selectedMessageIds ?? ' ');
                                showDeleteModal = false;
                                }}>Yes</button>
                            </div>
                          </div>
                        </form>
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
{/if}