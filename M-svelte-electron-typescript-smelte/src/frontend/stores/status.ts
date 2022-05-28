import { writable } from "svelte/store";

export let filePath=writable("");
export let totalDuration=writable(0);
export let startSecond=writable(0);
export let endSecond=writable(0);
// export let orgData:number[]|undefined|null=writable(number[]);
// export let orgDataLen:number|undefined|null=writable("");
// export let orgDataIdx:number[]|undefined|null=writable("");
// export let orgDataCircle:number[][]=[]=writable("");

export let orgData=writable([1]);
export let orgDataLen:any=writable([]);
export let orgDataIdx=writable([]);
export let orgDataCircle:any=writable([]);

export let filePathMulti=writable([]);

export let showWave=writable(false);