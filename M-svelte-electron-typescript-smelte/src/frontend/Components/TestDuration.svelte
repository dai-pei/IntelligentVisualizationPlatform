<script lang='ts'>
    import {filePath,totalDuration,startSecond,endSecond,orgData} from '../stores/status';
    let tempfilePath:any="";
    let tempstartSecond:number=-1;
    let tempendSecond:number=-1;
    let temptotalDuration:number;
    let temporgData:any;
    
    filePath.subscribe(value=>{
        tempfilePath=value;
    })
    totalDuration.subscribe(value=>{
        temptotalDuration=value;
    })
    startSecond.subscribe(value=>{
        tempstartSecond=value;
    })
    endSecond.subscribe(value=>{
        tempendSecond=value;
    })
    orgData.subscribe(value=>{
        temporgData=value;
    })

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

        filePath.set(file.path)
        console.log(tempfilePath)
    }

    function getDuration(){
        console.log(filePath);
        fetch(`http://127.0.0.1:6005/duration/`, {
            method: 'post',
            body:JSON.stringify({filepath:tempfilePath}),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((res) => {
            return res.json().then((response) => {
                console.log("response",response);
                totalDuration.set(response['duration']);
                console.log("totalduration",temptotalDuration);                
        });
      })
      .catch((error) => {
        console.error(error);
      });
    }

    function getSecondsAndOrgData(){
        fetch(`http://127.0.0.1:6005/orgdata/`, {
            method: 'post',
            body:JSON.stringify({filepath:tempfilePath,startsecond:tempstartSecond,endsecond:tempendSecond}),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((res) => {
            return res.json().then((response) => {
                orgData.set(response['loaddata']);           
                // console.log("orgdata response",temporgData); 
        });
      })
      .catch((error) => {
        console.error(error);
      });
    }

    function setSecondsAndOrgData(){
        startSecond.set(tempstartSecond);
        endSecond.set(tempendSecond);
        getSecondsAndOrgData();
        console.log(tempstartSecond,tempendSecond);
    }
</script>

<body>
    <input type = "file" on:change = {handleFileUploaded}/> 
    <button on:click={getDuration}>
        getDuration
    </button>
    <p>
        duration is : {temptotalDuration}
    </p>
    <form>
        <span>
            start second: {tempstartSecond}
        </span>
        <input type="text" bind:value={tempstartSecond}/>
        <span>
            end second: {tempendSecond}
        </span>
        <input type="text" bind:value={tempendSecond}/>
    </form>    
    <button on:click={setSecondsAndOrgData}>
        confirm time
    </button>

</body>