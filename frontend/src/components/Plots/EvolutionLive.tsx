import * as React from "react";
import Plot from 'react-plotly.js';
import { ExtrapolationResults } from "../../client"
import type { Data, PlotData } from "plotly.js";

/**
 * The "Evolution of Live Cells" plot 
 */
export function EvolutionLive({ extrapolationData }: { extrapolationData: ExtrapolationResults }) {
  if (typeof extrapolationData == "undefined") {
    return;
  }

  const generationPlots = extrapolationData.ext.cells_gen.data.map((data: any, generation: number): Partial<PlotData> => (
    {
      x: extrapolationData.ext.time_points.data,
      y: data,
      mode: "lines+markers",
      type: "scatter",
      name: `Generation ${generation}`
    }
  ));

  return (
    <div className="Plot">
      <Plot
        data={[
          {
            x: extrapolationData.ext.time_points.data,
            y: extrapolationData.ext.total_live_cells.data,
            mode: "lines+markers",
            type: "scatter",
            name: "Total Live Cells"
          },
          // {
          //   x: extrapolationData.hts.,
          //   y: extrapolationData.ext.total_live_cells.data,
          //   mode: "lines+markers",
          //   type: "scatter",
          //   name: "Harvest Times"
          // },
          ...generationPlots]
      }
        layout={{
          title: "Evolution of Live Cells",
          xaxis: {
            title: "Time (hours)",
          },
          yaxis: {
            title: "Cell Number",
          },
          autosize: true,  // Allow the chart to be responsive
        }}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}
