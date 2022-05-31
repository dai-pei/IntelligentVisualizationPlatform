<style>
  .hide-file-ui :global(input[type="file"]::file-selector-button) {
    display: none;
  }

  .hide-file-ui :global(:not(.mdc-text-field--label-floating) input[type="file"]) {
    color: transparent;
  }

  .demo-cell {
    height: 200px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: var(--mdc-theme-secondary, #333);
    color: var(--mdc-theme-on-secondary, rgb(245, 241, 241));
  }
</style>

<script lang="ts">
  import LayoutGrid, { Cell } from "@smui/layout-grid";
  import Textfield from "@smui/textfield";
  import Checkbox from "@smui/checkbox";
  import FormField from "@smui/form-field";
  import HelperText from "@smui/textfield/helper-text";
  import Button, { Label } from "@smui/button";

  let allFilePaths: any = null;
  let checkedZero = false;
  let checkedCent = false;
  let checkedMfcc = false;

  let textContent = "";
  let tempfilePathMulti: any[] = [];
  let classArr: any[] = [];

  function handleFilesUploaded() {
    textContent = "";
    for (var i = 0; i < allFilePaths.length; i++) {
      textContent += allFilePaths[i].name;
      textContent += "\n";

      let tempArr = new Array();
      tempArr.push(allFilePaths[i].path);
      if (allFilePaths[i].name.includes("Tom")) {
        tempArr.push("Tom");
      } else if (allFilePaths[i].name.includes("close")) {
        tempArr.push("close");
      } else if (allFilePaths[i].name.includes("open")) {
        tempArr.push("open");
      } else if (allFilePaths[i].name.includes("crash")) {
        tempArr.push("crash");
      } else if (allFilePaths[i].name.includes("kick")) {
        tempArr.push("kick");
      } else if (allFilePaths[i].name.includes("snare")) {
        tempArr.push("snare");
      }
      tempfilePathMulti.push(tempArr);

      if (classArr == null || classArr == [] || classArr.findIndex((value) => value == tempArr[1]) == -1) {
        classArr.push(tempArr[1]);
      }
    }
    console.log(classArr);
  }

  function showFeaturesChart() {
    console.log("showFeaturechart");
    var cnt = 0;
    if (checkedZero == true) {
      cnt++;
    }
    if (checkedCent == true) {
      cnt++;
    }
    if (checkedMfcc == true) {
      cnt++;
    }
    if (cnt != 2) {
      console.log("cnt " + String(cnt));
      alert("必须要勾选两个特征，不可以少于也不可多于2个！");
    } else {
      if (checkedZero == false) {
        console.log("requestFeaturesForKNN");
        requestFeaturesForKNN("cent", "mfcc");
      } else if (checkedCent == false) {
        console.log("requestFeaturesForKNN");
        requestFeaturesForKNN("zero", "mfcc");
      } else if (checkedMfcc == false) {
        console.log("requestFeaturesForKNN");
        requestFeaturesForKNN("cent", "zero");
      }
    }
  }

  function requestFeaturesForKNN(chosenfeature1: string, chosenfeature2: string) {
    fetch(`http://127.0.0.1:6005/featuresforknn/`, {
      method: "post",
      body: JSON.stringify({
        filepathmulti: tempfilePathMulti,
        classes: classArr,
        feature1: chosenfeature1,
        feature2: chosenfeature2,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => {
        return res.json().then((response) => {
          console.log(response);
          orgDataKNN = response["data"];
          console.log("orgDataKNN: ", orgDataKNN);

          // initVariables();
          // drawZeroCentKNN();
        });
      })
      .catch((error) => {
        console.error(error);
      });
  }
</script>

<body>
  <LayoutGrid>
    <Cell span="{12}">
      <div class="hide-file-ui">
        <input multiple variant="outlined" bind:files="{allFilePaths}" on:change="{handleFilesUploaded}" type="file" />
      </div>
    </Cell>
    <Cell span="{6}">
      <div class="demo-cell">
        <Textfield
          class="demo-cell"
          style="width: 80%;"
          helperLine$style="width: 80%;"
          disabled
          textarea
          bind:value="{textContent}"
          label="FilePaths"
          invalid
        >
          <HelperText slot="helper">选中的音频路径</HelperText>
        </Textfield>
      </div>
    </Cell>
    <Cell span="{6}">
      <div class="feature-checkboxes">
        <FormField class="demo-cell">
          <Checkbox bind:checkedZero />
          <span slot="label">过零率</span>
        </FormField>
        <FormField class="demo-cell">
          <Checkbox bind:checkedCent />
          <span slot="label">频谱质心</span>
        </FormField>
        <FormField class="demo-cell">
          <Checkbox bind:checkedMfcc />
          <span slot="label">MFCC</span>
        </FormField>
      </div>
      <div class="comfirm-button">
        <Button on:click{showFeaturesChart} variant="outlined">
          <Label>生成二维特征数组</Label>
        </Button>
      </div>
    </Cell>
  </LayoutGrid>
</body>
