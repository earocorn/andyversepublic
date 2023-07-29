<script lang="ts">
	import '../routes/styles/Header.css';
	import { afterUpdate, onDestroy, onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { routes } from '../server/config/routes';
	import { onAuthStateChanged } from 'firebase/auth';
	import { auth } from '../server/config/firebase';
	import { currentUser } from '../server/stores';
	import type User from '../server/models/AndyVerseUser';
	import { handleSignOut, populateUserStores } from '../server/authentication/authenticator';
	import { browser } from '$app/environment';

	// TEARS OF PAIN
	export let userData;

	let active = '';

	let signedInUser: User | null = null;
	
	let firebaseUser = browser ? localStorage.getItem('user') : null;
	let firebaseUserData = firebaseUser ? JSON.parse(firebaseUser) : userData.firebaseUserData;
	let dbUser = browser ? localStorage.getItem('dbUserData') : userData.dbUserData;
	let dbUserData = dbUser ? JSON.parse(dbUser) : null;

	onMount(() => {
		const pathFormatted = location.pathname.split('/')[1];
		if (location.pathname === '/' || !pathFormatted) {
			try {
				if (!routes[0].includes(pathFormatted)) {
					goto('/home');
					active = 'home';
				}
			} catch (error) {
				console.error(error);
			}
		} else {
			active = pathFormatted;
		}

		currentUser.subscribe((value) => {
			signedInUser = value;
		});
        onAuthStateChanged(auth, async (user) => {
            if(user) {
				if(browser) {
					localStorage.setItem('user', JSON.stringify(user));
					const andyUser = await populateUserStores(user);
					dbUserData = andyUser;
					firebaseUserData = firebaseUser ? JSON.parse(firebaseUser) : null;
				}
            } else {
				if(browser) {
					dbUserData = null;
					firebaseUserData = null;
					localStorage.removeItem('user');
					localStorage.removeItem('dbUserData');
				}
			}
        });
	});

	afterUpdate(() => {
		if(auth.currentUser) {
			populateUserStores(auth.currentUser);
		}
	})

	const unsubscribe = page.subscribe((value) => {
		let path = value.url.pathname;
		path = path.replace('/', '');
		path = path.replaceAll('_', ' ');
		active = path;
	});

	onDestroy(() => unsubscribe());
</script>

<div>
	<div class="navbar w-full">
		<div class="navbar start">
			<div class="dropdown">
				<!-- svelte-ignore a11y-label-has-associated-control -->
				<label tabindex="-1" class="btn btn-ghost hidden-lg">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-5 w-5"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						><path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M4 6h16M4 12h8m-8 6h16"
						/></svg
					>
				</label>
				<ul
					tabindex="-1"
					class="menu bg-secondary dropdown-content mt-3 z-[1] shadow rounded-box w-52"
				>
                    {#each routes as tab}
						{#if tab[2] === 'public'}
							<li><a href={'/' + tab[0]}>{tab[1]}</a></li>
						{/if}
					{/each}
				</ul>
			</div>
			<a href="/home" class="btn btn-ghost text-xl" style="font-size: x-large;">The AndyVerse</a>
		</div>

		<div class="navbar-center hidden lg:flex">
			<ul class="menu menu-horizontal px-1">
				<div class="tabs">
					{#each routes as tab}
						{#if tab[2] === 'public'}
							<a
								class="tab tab-bordered {active === tab[0] ? 'tab-active' : ''}"
								href={'/' + tab[0]}>{tab[1]}</a
							>
						{/if}
					{/each}
				</div>
			</ul>
		</div>

		<div class="navbar-end">
			{#if browser && auth.currentUser && signedInUser}
				<div class="dropdown">
					<!-- svelte-ignore a11y-label-has-associated-control -->
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<!-- svelte-ignore a11y-no-static-element-interactions -->
					<label tabindex="-1" class="btn btn-ghost">
						Signed in as<span class="link"
							>{signedInUser?.username ? signedInUser.username : auth.currentUser.email}</span
						>
						<svg
							width="12px"
							height="12px"
							class="h-2 w-2 fill-current opacity-60 inline-block"
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 2048 2048"
							><path d="M1799 349l242 241-1017 1017L7 590l242-241 775 775 775-775z" /></svg
						>
					</label>
					<ul tabindex="-1" class="menu dropdown-content shadow px-1">
						<li><a href="/profile">My Profile</a></li>
						<!-- svelte-ignore a11y-invalid-attribute -->
						<li class="bg-primary"><a on:click={handleSignOut} href="#">Sign Out</a></li>
					</ul>
				</div>
			{:else if active !== 'login'}
				<a href="/login" class="btn btn-primary" style="font-weight: bold;"
					>Sign In</a
				>
			{/if}
		</div>
	</div>
</div>
