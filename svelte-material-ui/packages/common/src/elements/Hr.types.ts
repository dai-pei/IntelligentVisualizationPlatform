import type Component from './Hr.svelte';

export declare class HrComponentDev extends Component {
  /**
   * @private
   * For type checking capabilities only.
   * Does not exist at runtime.
   * ### DO NOT USE!
   */
  $$prop_def: Omit<Partial<svelte.JSX.HTMLAttributes<HTMLHRElement>>, 'use'> &
    Component['$$prop_def'];
}
