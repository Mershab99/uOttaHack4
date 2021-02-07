import "./App.css";
import { useEffect } from "react";
import { useRef } from "react";

function Message(props) {
  return (
    <div
      style={{
        color: "black",
        fontSize: "370%",
        fontFamily: "Century Gothic",
        textAlign: "center",
        marginTop: 50,
        marginBottom: 50,

        // if they are wearing a mask
        // if they are not wearing a mask
        // if they did not sanatize their hands
        // scenario for if they did both
      }}
    >
      {props.msg}
    </div>
  );
}

function MaskAndSanitize() {
  return (
    <div>
      <img
        src="all.jpg"
        alt="thanks"
        width="1000%"
        height="1000%"
        className="thanks"
      />
    </div>
  );
}

function NoMask() {
  return (
    <div>
      <img
        src="noMask.png"
        alt="noMask"
        width="1000%"
        height="1000%"
        className="thanks"
      />
    </div>
  );
}


function App() {
  let sanitizedHands = true;
  let maskOn = true;

  if (sanitizedHands === true && maskOn === true) {
    return (
      <div>
        <MaskAndSanitize />
        <Footage />
      </div>
    );
  } else if (sanitizedHands === true && maskOn === false) {
    return <NoMask />;
  } else if (sanitizedHands === false && maskOn === true) {
    return <MaskAndSanitize />;
  } else if (sanitizedHands === false && maskOn === false) {
    return <NoMask />;
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
    [20, 40, 60, 70],
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
    context.fillStyle = "black";
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

const inputs = document.querySelectorAll(".input");

function addcl() {
  let parent = this.parentNode.parentNode;
  parent.classList.add("focus");
}

function remcl() {
  let parent = this.parentNode.parentNode;
  if (this.value == "") {
    parent.classList.remove("focus");
  }
}

inputs.forEach((input) => {
  input.addEventListener("focus", addcl);
  input.addEventListener("blur", remcl);
});

//num peole in store and stats
//walking in zone and social distancing circle
export default App;

{
  /* <div>
<form action="/action_page.php">
  <label for="wstrtx">Walkzone Start X:</label>
  <input type="text" id="wstrtx" name="wstrtx" />
  <label for="wendx">Walkzone End X:</label>
  <input type="text" id="wendx" name="wendx" />
  <label for="wstrty">Walkzone Start Y:</label>
  <input type="text" id="wstrty" name="wstrty" />
  <label for="wstrtx">Walkzone End Y:</label>
  <input type="text" id="wendy" name="wendy" />
  <label for="sstrtx">Sanitizer Start X:</label>
  <input type="text" id="sstrtx" name="sstrtx" />
  <label for="sendx">Sanitizer End X:</label>
  <input type="text" id="sendx" name="sendx" />
  <label for="sstrty">Sanitizer Start Y:</label>
  <input type="text" id="sstrty" name="sstrty" />
  <label for="sendx">Sanitizer End Y:</label>
  <input type="text" id="sendy" name="sendy" />
  <input type="submit" value="Submit" />
</form>
</div> */
}
