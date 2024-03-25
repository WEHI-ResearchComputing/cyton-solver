import * as React from "react";
import Slider from "../Slider/Slider";

export default function ParameterForm() {
  return (
      <form>
        <Slider label="mDD"/>
        <Slider label="sDD"/>
        <Slider label="mDie"/>
        <Slider label="sDie"/>
        <Slider label="mDiv0"/>
        <Slider label="sDiv0"/>
        <Slider label="mUns"/>
        <Slider label="sUns"/>
        <Slider label="b"/>
        <Slider label="p"/> 
      </form>
  )
}
