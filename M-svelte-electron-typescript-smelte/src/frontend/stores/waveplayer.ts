import { writable } from "svelte/store"
import WavePlayer from "../logic/waveplayer"

export let MediaPlayer=writable(new WavePlayer)