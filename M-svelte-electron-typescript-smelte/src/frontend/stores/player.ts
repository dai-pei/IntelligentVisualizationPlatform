import { writable } from 'svelte/store';
import Player from '../logic/player'

export let MediaPlayer = writable(new Player);

export let SiteContentBind = writable();