import * as React from "react";
import { useForm, SubmitHandler, Controller, FormProvider, useFormContext } from "react-hook-form"
import type { Parameters } from "../../client"
import { Tooltip } from "@mui/material";
import Slider from "../Slider/Slider"

export default function ParameterForm() {
  return (
      <form>
        {/* <Tooltip title="Median time to division destiny" >
          <Controller
            name="mDD"
            control={control}
            render={({ field }) => <Slider
              label="mdd"
              {...field}
              />}
          ></Controller>
          { <SliderElement max={100} label="mDD" label="mDD")}/> }
        </Tooltip> */}
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
        <input type="submit" />
      </form>
  )
}
