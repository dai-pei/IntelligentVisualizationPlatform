import { writable } from "svelte/store";

export const right = writable(false);
export const persistent = writable(true);
export const elevation = writable(false);
export const showNav = writable(true);
export const dark = writable(false);

let basePath:any;

function init() {
    basePath = document.getElementsByTagName('base')[0].getAttribute('href')!;
    if (basePath && basePath.length > 0 && basePath[basePath.length - 1] === '/') {
        basePath = basePath.substring(0, basePath.length - 1);
    }
    console.log('basePath: ', basePath);
}

function fixPathName(path: string) {
    if (basePath) {
        return path.substring(basePath.length);
    }
    return path;
}

function addBasePath(items: { to: string, text:string }[]) {
    return items.map(x => ({ to: basePath + x.to, text: x.text }));
}

export { basePath, init, fixPathName, addBasePath };