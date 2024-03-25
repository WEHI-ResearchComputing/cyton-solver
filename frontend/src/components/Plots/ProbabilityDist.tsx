import * as React from "react";
import Plot from 'react-plotly.js';
import { ExtrapolationResults } from "../../client"
import type { PlotData } from "plotly.js";

export function ProbabilityDist({ extrapolationData }: { extrapolationData: ExtrapolationResults }) {
  return (
    <div className="Plot">
      <Plot
        data={Object.entries(extrapolationData.ext.densities).map(([rv, densities]) : Partial<PlotData> => ({
          name: `${rv} Density`,
          x: extrapolationData.ext.time_points,
          y: densities.data
        }))}
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
