import logo from "./logo.svg";
import "./App.css";
import { useEffect } from "react";
import { useRef } from "react";

function Message(props) {
  return (
    <div
      style={{
        color: "white",
        fontSize: "370%",
        fontFamily: "dosis",
        textAlign: "center",
      }}
    >
      {props.msg}
    </div>
  );
}

function SanitizedHands() {
  return <Message msg="Thank you for washing your hands!" />;
}

function NoPurell() {
  return <Message msg="Missing sanatizer" />;
}

function App() {
  let sanitizedHands = true;

  if (sanitizedHands === true) {
    return (
      <div>
        <SanitizedHands />
        <Footage />
      </div>
    );
  } else if (sanitizedHands === false) {
    return <NoPurell />;
  }
}

const getPixelRatio = (context) => {
  var backingStore =
    context.backingStorePixelRatio ||
    context.webkitBackingStorePixelRatio ||
    context.mozBackingStorePixelRatio ||
    context.msBackingStorePixelRatio ||
    context.oBackingStorePixelRatio ||
    context.backingStorePixelRatio ||
    1;

  return (window.devicePixelRatio || 1) / backingStore;
};

function Footage() {
  let coords = [
    [20, 40, 50, 80],
    [20, 30, 40, 60],
    [62, 64, 420, 420],
  ];
  let ref = useRef();
  let tl = [20, 40];
  let br = [60, 70];

  useEffect(() => {
    // Initialize canvas
    let canvas = ref.current;
    let context = canvas.getContext("2d");

    // Fix resolution
    let ratio = getPixelRatio(context);
    let width = getComputedStyle(canvas).getPropertyValue("width").slice(0, -2);
    let height = getComputedStyle(canvas)
      .getPropertyValue("height")
      .slice(0, -2);
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;

    // Draw the background
    context.fillStyle = "white";
    context.fillRect(0, 0, 100000, 100000);

    // Draw the store
    const img = new Image();
    img.src = "./store.jpg";

    img.onload = () => {
      context.drawImage(img, 0, 0);

      // Draw the bounding boxes
      for (let i = 0; i < coords.length; i++) {
        let curr = coords[i];

        context.beginPath();
        context.lineWidth = "1";
        context.strokeStyle = "black";
        context.rect(curr[1], curr[0], curr[3], curr[2]);
        context.stroke();
      }
    };
  });

  return (
    <div>
      <img href="store.jpg"></img>
      <canvas
        ref={ref}
        style={{
          width: "50%",
          height: "50%",
        }}
      />
    </div>
  );
}

//num peole in store and stats
//walking in zone and social distancing circle
export default App;
