import Card from "@/components/card/card";
import "./module.css";

export default function LoadingCard() {
  return (
    <Card>
<div className="cardContent">
        {/* LEFT COLUMN */}
        <div className="leftColumn">
          <div className="SessionBox">
            
            <div className="loading-1">  </div>
            <div className = "loading-2"> </div>
            <div className = "loading-3"> </div>
            </div>




          
          <div className = 'loading-button'>

          </div>
        </div>

        {/* RIGHT COLUMN */}
        <div className="rightColumn">
          <div className="statusBox">
            <div className ="loading-4"></div>
          </div>
          <div className="dateBox">
           <div className ="loading-5"></div>
          </div>

          <div className="gauge">
            <div className="gauge-ring">
              {/* 5 loading segments */}
              <div className="gauge-segment gauge-segment-1 gauge-segment--loading" />
              <div className="gauge-segment gauge-segment-2 gauge-segment--loading" />
              <div className="gauge-segment gauge-segment-3 gauge-segment--loading" />
              <div className="gauge-segment gauge-segment-4 gauge-segment--loading" />
              <div className="gauge-segment gauge-segment-5 gauge-segment--loading" />
            </div>

        {/* center letter or leave empty */}
        <div className="loading-grade"></div>
      </div>



        </div>
      </div>
      
    </Card>
  )
}


