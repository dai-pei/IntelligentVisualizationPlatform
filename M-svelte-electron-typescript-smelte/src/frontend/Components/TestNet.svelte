<script lang="ts">
    let filePath: any="s"
    var formData = new FormData();
    async function requestLoadData() {
        console.log(filePath);
        // let str:string='filepath:null'
        formData.append("filepath",filePath);
        let temp:any=JSON.stringify({filepath:filePath});
        console.log(temp);
        // const res = await fetch(``);
        // const res=fetch(`http://127.0.0.1:6005/orgdata/`, {
        //     method: 'post',
        //     // body:"filepath="+filePath,
        //     body:JSON.stringify({filepath:filePath}),
        //     // body:new URLSearchParams([["filepath",filePath]]).toString(),
        //     headers: {
        //         'Content-Type': 'application/json'
        //         // 'Content-Type': 'application/x-www-form-urlencoded'
        //     }
        // });
	    // let photos:any = await 
        // console.log("photos:",photos);

        fetch(`http://127.0.0.1:6005/orgdata/`, {
            method: 'post',
            // body:"filepath="+filePath,
            body:JSON.stringify({filepath:filePath}),
            // body:new URLSearchParams([["filepath",filePath]]).toString(),
            headers: {
                'Content-Type': 'application/json'
                // 'Content-Type': 'application/x-www-form-urlencoded'
            }
        }).then((res) => {
            return res.json().then((response) => {
                console.log("json loaddata")
                console.log(response["loaddata"]);
        });
      })
      .catch((error) => {
        console.error(error);
      });
    }
    async function requestNet() {
        console.log(filePath);
        const res = await fetch(`http://127.0.0.1:6005/`);
	    let photos:string = await res.json();
        console.log(photos)
    }

    function handleFileUploaded(e:Event){
        const target = e.target as HTMLInputElement;
        const files = target.files;
        if (!files) {
            console.log(1);
            return;
        }

        const file = files[0];
        if (!file) {
            console.log(2);
            return;
        }

        console.log(file)
        console.log(file.path)

        filePath=file.path

        console.log(filePath)
    }

</script>

<input type = "file" on:change = {handleFileUploaded}/> 
<button on:click = {requestLoadData} > load data </button>
<button on:click = {requestNet} > 测试网络 </button>