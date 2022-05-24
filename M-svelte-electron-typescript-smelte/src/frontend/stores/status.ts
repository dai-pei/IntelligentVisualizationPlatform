import { writable } from "svelte/store";

export let filePath:any=writable("");
// export let orgData:number[]|undefined|null=writable(number[]);
// export let orgDataLen:number|undefined|null=writable("");
// export let orgDataIdx:number[]|undefined|null=writable("");
// export let orgDataCircle:number[][]=[]=writable("");
export let orgData:any=writable([]);
export let orgDataLen:any=writable([]);
export let orgDataIdx=writable([]);
export let orgDataCircle:any=writable([]);

