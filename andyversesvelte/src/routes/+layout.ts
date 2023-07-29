import { browser, dev } from "$app/environment";

export const prerender = true;

/** @type {import('./$types').LayoutPageLoad} */
export function load() {
    if(browser) {
        const firebaseUser = localStorage.getItem('user');
        const firebaseUserData = firebaseUser !== null ? JSON.parse(firebaseUser) : null;
        const dbUser = localStorage.getItem('dbUserData');
        const dbUserData = dbUser !== null ? JSON.parse(dbUser) : null;
        if(firebaseUserData && dbUserData) {
            return {
                userData: {
                    firebaseUserData: firebaseUserData,
                    dbUserData: dbUserData,
                },
            };
        } else {
            return {
                userData: 'No current user'
            }
        }
    }
}