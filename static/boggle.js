class BoggleGame {
  constructor() {
    this.alreadyFound = new Set();
    this.score = 0;
    this.nOfPlay = 0;
    this.showtimer();
    $("#form-input").on("submit", this.handleSubmit.bind(this));
  }

  // Checks the validity of the word, stores it and handles the UI
  async handleSubmit(e) {
    e.preventDefault();
    const word = $("#guess").val();
    console.log(word);
    console.log(this.alreadyFound);
    if (this.alreadyFound.has(word)) {
      this.showMessage(`${word} already added! Choose a unique word`);
    } else {
      const res = await axios.get("/check-word", { params: { word: word } });
      console.log(res.data);

      // check if the word if valid
      if (res.data.result === "not-word") {
        this.showMessage("The word is not a valid word");
      } else if (res.data.result === "not-on-board") {
        this.showMessage("The word does not exist on the board");
      } else {
        this.showMessage("The word exists on the board!");
        this.score += word.length;
        this.alreadyFound.add(word);
      }
    }
    this.showScore();
    this.handleScore();
    console.log(this.alreadyFound);
  }

  // Show the validity of the word on the UI
  showMessage(msg) {
    $(".message").text(msg);
  }

  // Update the score on the UI
  showScore() {
    $(".score").text(this.score);
  }

  //Store new score and updates the UI
  async handleScore() {
    const res = await axios.post("/store-score", { score: this.score });
    console.log(res);
  }

  //Sets the time limit for the game
  showtimer() {
    let time = 60;
    let timerDiv = $("#timer");
    let self = this;
    self.interval = setInterval(function () {
      timerDiv.text(`${time}`);
      time -= 1;

      if (time < 0) {
        clearInterval(self.interval);
        self.toggleAllowSubmit(false);
      }
    }, 1000);
  }

  toggleAllowSubmit(isEnabled) {
    console.log(isEnabled);
    $(".submit-btn").prop("disabled", !isEnabled);
  }
}
