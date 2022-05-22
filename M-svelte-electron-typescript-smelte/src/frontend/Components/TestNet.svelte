<script lang="ts">
    let filePath: string | null | undefined = "";
    let base:string='{\'name\':\'test\'}';
    async function requestLoadData() {
        console.log(filePath);
        // const res = await fetch(``);
        const res=fetch(`http://127.0.0.1:6005/login`, {
            method: 'post',
            body: JSON.stringify(base),
            headers: {
            'Content-Type': 'application/json'
            }
        });
	    let photos:any = await res;
        console.log(photos);
    }
    async function requestNet() {
        console.log(filePath);
        const res = await fetch(`http://127.0.0.1:6005/`);
	    let photos:string = await res.json();
        console.log(photos)
    }

</script>

<input type = "file" bind:value = {filePath}/> 
<button on:click = {requestLoadData} > 请求网络 </button>
<button on:click = {requestNet} > 请求网络 </button>