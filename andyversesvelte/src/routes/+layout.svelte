<script lang="ts">
	import '../app.css';
	import 'daisyui/dist/full.css';
	import Header from '../components/Header.svelte';
	import Footer from '../components/Footer.svelte';
	import Main from '../components/Main.svelte';
	import { goto } from '$app/navigation';
	import { isAdmin, populateUserStores } from '../server/authentication/authenticator';
	import { routes } from '../server/config/routes';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';
	import { auth } from '../server/config/firebase';
	
	export let data;
	let userData = data;

	onMount(async () => {
		const authenticated = await new Promise((resolve, reject) => {
        const unsubscribe = auth.onAuthStateChanged(user => {
            	unsubscribe(); // Unsubscribe after the initial state is received
            	resolve(user ? true : false);
			}, error => {
				unsubscribe(); // Unsubscribe in case of an error
				reject(error);
			});
		});
		if(auth.currentUser) {
			populateUserStores(auth.currentUser);
		}

		const admin = await isAdmin();
		const pathFormatted = location.pathname.split('/')[1];
		let active = pathFormatted;
		const activeRoute = routes.find((route) => route[0] === active);
		if(activeRoute) {
			if(activeRoute[2] === 'private') {
				if(!authenticated) {
					if(browser) {
					goto('/home');
					}
				}
			} else if(activeRoute[2] === 'admin') {
				if(!authenticated) {
					if(browser) {
					console.error('Not authenticated trying to access admin-only.')
					goto('/home');
					}
				}
				if(!admin) {
					if(browser) {
					console.error('Not admin!!!')
					goto('/home');
					}
				}
			}
		}
	})
	
</script>

<header class="sticky top-0 z-50">
	<Header userData={userData}/>
</header>

<main>
	<Main>
		<div class="flex-grow p-2">
				<slot />
		</div>
		<Footer />
	</Main>
</main>
