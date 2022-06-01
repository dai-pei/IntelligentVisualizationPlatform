<script>
    import { Router, Route } from "svelte-routing";
    import NavLink from "./NavLink.svelte";
    import UploadMusic from "./UploadMusic.svelte";
    import ShowFeatures from "./ShowFeatures.svelte";
    import DoClassify from "./DoClassify.svelte";
    import BasicAudioProcessing from "./BasicAudioProcessing.svelte";
  
    // Used for SSR. A falsy value is ignored by the Router.
    export let url = "";
  </script>

<Router url="{url}">
    <nav>
      <NavLink to="basicknowledge">了解声音</NavLink>
      <NavLink to="wave">加载音乐</NavLink>
      <NavLink to="feature">特征解析</NavLink>
      <NavLink to="classify">进行分类</NavLink>
    </nav>
    <div>
      <Route path="basicknowledge" component="{BasicAudioProcessing}" />
      <Route path="wave" component="{UploadMusic}" />
      <Route path="feature" component="{ShowFeatures}" />
      <Route path="classify" component="{DoClassify}" />
    </div>
  </Router>
  