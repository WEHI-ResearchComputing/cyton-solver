import * as React from "react";
import Plot from 'react-plotly.js';
import { ExtrapolationResults } from "../../client"
import type { Data, PlotData } from "plotly.js";

export function CellsVsGens({ extrapolationData }: { extrapolationData: ExtrapolationResults }) {

  return (
    <div className="Plot">
      <Plot
        data={extrapolationData.}
        layout={{
          title: "Probability Distribution",
          xaxis: {
            title: "Time (hours)",
          },
          yaxis: {
            title: "Density",
          },
          autosize: true,  // Allow the chart to be responsive
        }}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}
