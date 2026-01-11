const NUM_SLIDERS = 4;

//////////////////////////////////////////////////////////////////////////////////////
async function matchupButton() {
  // *** Pass inputs ***
  const batter = document.getElementById("batter-dropdown").value;
  const pitcher = document.getElementById("pitcher-dropdown").value;

  // *** Call API ***
  const response = await fetch(
    `http://localhost:8000/matchup?batter=${batter}&pitcher=${pitcher}`
  );
  const data = await response.json();

  // *** Configure returns ****

  // Automatically paritally reset for user in case matchup configuration is not manually reset before re-prompt
  resetButton(false);

  // Configure score and message
  const scoreSpan = document.getElementById("grand-score");
  const grandScore = data.grand_score.toFixed(3);
  scoreSpan.innerText = " " + String(grandScore) + " RV/100";
  const batterDropdown = document.getElementById("batter-dropdown");
  const batterName =
    batterDropdown.options[batterDropdown.selectedIndex].innerText;
  const pitcherDropdown = document.getElementById("pitcher-dropdown");
  const pitcherName =
    pitcherDropdown.options[pitcherDropdown.selectedIndex].innerText;
  const msgWinner = document.getElementById("message-winner");
  const msgLoser = document.getElementById("message-loser");
  if (grandScore > 0.0) {
    scoreSpan.style.color = "blue";
    msgWinner.style.color = "blue";
    msgWinner.innerText = batterName;
    msgLoser.style.color = "red";
    msgLoser.innerText = pitcherName;
  } else if (grandScore < 0.0) {
    scoreSpan.style.color = "red";
    msgWinner.style.color = "red";
    msgWinner.innerText = pitcherName;
    msgLoser.style.color = "blue";
    msgLoser.innerText = batterName;
  }
  const msgScoreMargin = document.getElementById("message-score-margin");
  if (Math.abs(grandScore) >= 1.0) {
    msgScoreMargin.innerText = " excellent";
    msgScoreMargin.style.color = "rgb(0, 255, 0)";
  } else if (Math.abs(grandScore) >= 0.5) {
    msgScoreMargin.innerText = " great";
    msgScoreMargin.style.color = "rgb(246, 255, 0)";
  } else if (Math.abs(grandScore) >= 0.1) {
    msgScoreMargin.innerText = " good";
    msgScoreMargin.style.color = "rgb(255, 140, 0)";
  } else {
    msgScoreMargin.innerText = " okay";
    msgScoreMargin.style.color = "rgb(75, 75, 75)";
  }

  // ** Configure pitch sliders **

  // Configure pitch-type score
  const arsenalScoreSpan = document.getElementById("arsenal-score");
  const pitchTypeGrandScore = data.grand_pitch_type_score.toFixed(3);
  arsenalScoreSpan.innerText = String(pitchTypeGrandScore) + " RV/100";
  if (pitchTypeGrandScore > 0.0) {
    arsenalScoreSpan.style.color = "blue";
  } else if (pitchTypeGrandScore < 0.0) {
    arsenalScoreSpan.style.color = "red";
  }

  // Load additional sliders (if necessary)
  const scoredPitchTypes = data.pitch_type_scores;
  const pitchFreqs = data.pitch_type_frequencies;
  loadSliders(Object.keys(scoredPitchTypes).length + 1 - NUM_SLIDERS);

  // Configure sliders
  const pitchLabels = document.getElementsByClassName("pitch-type-field");
  const pitchTypeSubScores = document.getElementsByClassName(
    "pitch-type-sub-score-field"
  );
  const sliderIndicators = document.getElementsByClassName("slider-indicator");
  var i = 0;
  for (const [p, s] of Object.entries(scoredPitchTypes)) {
    // Configure location of slider-indicators
    pitchLabels[i].innerText =
      p + " (" + String((pitchFreqs[p] * 100).toFixed(1)) + "%)";
    if (s > 2.0) {
      sliderIndicators[i].style.left = "100%";
      document.getElementById("sliders-container").children[
        i
      ].style.outlineColor = "blue";
    } else if (s < -2.0) {
      sliderIndicators[i].style.left = "0%";
      document.getElementById("sliders-container").children[
        i
      ].style.outlineColor = "red";
    } else {
      sliderIndicators[i].style.left = String(Math.ceil(50 * s)) + "%"; // s' = s(100/2); always round up to avoid 0%'s
    }

    // Configure color-coding of slider-indicators
    if (Math.abs(s) >= 1.0) {
      sliderIndicators[i].style.backgroundColor = "rgb(0, 255, 0)";
    } else if (Math.abs(s) >= 0.5) {
      sliderIndicators[i].style.backgroundColor = "rgb(246, 255, 0)";
    } else if (Math.abs(s) >= 0.1) {
      sliderIndicators[i].style.backgroundColor = "rgb(255, 140, 0)";
    } else {
      sliderIndicators[i].style.backgroundColor = "rgb(75, 75, 75)";
    }

    // Configure slider sub-scoring and their color-codings
    pitchTypeSubScores[i].innerText = String(s.toFixed(3)) + " RV/100";
    if (s > 0.0) {
      pitchTypeSubScores[i].style.color = "blue";
      sliderIndicators[i].style.outlineColor = "blue";
    } else if (s < 0.0) {
      pitchTypeSubScores[i].style.color = "red";
      sliderIndicators[i].style.outlineColor = "red";
    }

    i++;
  }

  // ** Configure zone cells **

  // Configure zone score
  const locationScoreSpan = document.getElementById("location-score");
  const zoneGrandScore = data.grand_zone_score.toFixed(3);
  locationScoreSpan.innerText = String(zoneGrandScore) + " RV/100";
  if (zoneGrandScore > 0.0) {
    locationScoreSpan.style.color = "blue";
  } else if (zoneGrandScore < 0.0) {
    locationScoreSpan.style.color = "red";
  }

  // Configure zone cells
  const scoredZones = data.zone_scores;
  const gridSubScores = document.getElementsByClassName("grid-sub-score");
  const gridCells = document.getElementsByClassName("grid-cell");
  const shadowSubScores = document.getElementsByClassName("shadow-sub-score");
  const shadowCells = document.getElementsByClassName("shadow-cell");
  const wasteSubScores = document.getElementsByClassName("waste-sub-score");
  const wasteCells = document.getElementsByClassName("zone-waste");
  var idx = 0;
  var subScores = gridSubScores;
  var cells = gridCells;
  for (const s of Object.values(scoredZones)) {
    // Select suitable structures
    if (idx < 9) {
      i = idx;
    } else if (idx < 17) {
      subScores = shadowSubScores;
      cells = shadowCells;
      i = idx - 9;
    } else {
      subScores = wasteSubScores;
      cells = wasteCells;
      i = idx - 17;
    }

    // Configure color-coding of cell borders
    if (Math.abs(s) >= 1.0) {
      cells[i].style.borderColor = "rgb(0, 255, 0)";
    } else if (Math.abs(s) >= 0.5) {
      cells[i].style.borderColor = "rgb(246, 255, 0)";
    } else if (Math.abs(s) >= 0.1) {
      cells[i].style.borderColor = "rgb(255, 140, 0)";
    } else {
      cells[i].style.borderColor = "rgb(75, 75, 75)";
    }

    // Configure sub-scoring and color-coding of zone-cells
    if ([9, 10, 17].includes(idx)) {
      subScores[i].innerText = String(s.toFixed(3)) + " RV/100";
    } else {
      subScores[i].innerText = String(s.toFixed(3)) + "\nRV/100";
    }
    if (s > 0.0) {
      cells[i].style.backgroundColor =
        "rgb(0, 0, " + String(155 + s * 50) + ")"; // s' = 155 + s(100/2); scaled from 155 to 255 as is the only range cosmetically significant
    } else if (s < 0.0) {
      cells[i].style.backgroundColor =
        "rgb(" + String(155 + s * 50) + ", 0, 0)";
    }

    idx++;
  }
}

//////////////////////////////////////////////////////////////////////////////////////

async function resetButton(fullReset = true) {
  for (const elem of document.getElementsByClassName("dynamic-color")) {
    elem.style.color = "rgba(93, 93, 93, 1)";
    elem.innerText = "---";
  }
  if (fullReset) {
    document.getElementById("batter-dropdown").value = "select";
    document.getElementById("pitcher-dropdown").value = "select";
  }

  unloadSliders();

  const pitchLabels = document.getElementsByClassName("pitch-field");
  for (const l of pitchLabels) {
    l.innerText = "XX";
  }

  const pitchTypeSubScores = document.getElementsByClassName(
    "pitch-type-sub-score"
  );
  for (const s of pitchTypeSubScores) {
    s.innerText = "-";
    s.style.color = "gray";
  }

  const sliderIndicators = document.getElementsByClassName("slider-indicator");
  for (const i of sliderIndicators) {
    i.style.outlineColor = "gray";
    i.style.left = "50%";
  }

  const gridCells = document.getElementsByClassName("grid-cell");
  for (const c of gridCells) {
    c.style.backgroundColor = "rgb(55, 55, 55)";
  }
  const gridSubScores = document.getElementsByClassName("grid-sub-score");
  for (const c of gridSubScores) {
    c.style.color = "white";
    c.innerText = "-";
  }

  const shadowCells = document.getElementsByClassName("shadow-cell");
  for (const c of shadowCells) {
    c.style.backgroundColor = "rgb(55, 55, 55)";
  }
  const shadowSubScores = document.getElementsByClassName("shadow-sub-score");
  for (const c of shadowSubScores) {
    c.style.color = "white";
    c.innerText = "-";
  }

  const wasteCells = document.getElementsByClassName("zone-waste");
  for (const c of wasteCells) {
    c.style.backgroundColor = "rgb(55, 55, 55)";
  }
  const wasteSubScores = document.getElementsByClassName("waste-sub-score");
  for (const c of wasteSubScores) {
    c.style.color = "white";
    c.innerText = "-";
  }
}

//////////////////////////////////////////////////////////////////////////////////////
async function loadDropdowns() {
  const response = await fetch(`http://localhost:8000/players`);
  const data = await response.json();
  const batters = data.batters;
  const pitchers = data.pitchers;
  batters.sort((a, b) => a.standard_name.localeCompare(b.standard_name));
  pitchers.sort((a, b) => a.standard_name.localeCompare(b.standard_name));

  const template = document.getElementById("dropdown-subject-template").content
    .firstElementChild;

  const batterDropdown = document.getElementById("batter-dropdown");
  for (b of batters) {
    const dropdownSubject = template.cloneNode(true);
    dropdownSubject.style.display = "block";
    dropdownSubject.value = b.snake;
    dropdownSubject.innerText = b.standard_name;
    batterDropdown.appendChild(dropdownSubject);
  }

  const pitcherDropdown = document.getElementById("pitcher-dropdown");
  for (p of pitchers) {
    const dropdownSubject = template.cloneNode(true);
    dropdownSubject.style.display = "block";
    dropdownSubject.value = p.snake;
    dropdownSubject.innerText = p.standard_name;
    pitcherDropdown.appendChild(dropdownSubject);
  }
}

async function loadSliders(n) {
  const template =
    document.getElementById("slider-template").content.firstElementChild;
  const sliderContainer = document.getElementById("sliders-container");
  var i = 0;
  while (i < n) {
    const slider = template.cloneNode(true);
    slider.style.display = "block";
    sliderContainer.appendChild(slider);
    i++;
  }
}

async function unloadSliders() {
  const sliderContainer = document.getElementById("sliders-container");
  const sliders = sliderContainer.children;
  while (sliders.length > 4) {
    sliders[1].remove();
  }
}

async function loadCells() {
  var template =
    document.getElementById("grid-cell-template").content.firstElementChild;
  const innerGrid = document.getElementById("zone-grid");
  var i = 0;

  while (i < 9) {
    const cell = template.cloneNode(true);
    cell.style.display = "block";
    innerGrid.appendChild(cell);
    i++;
  }
}

// LOOK: Currently disabled.
// async function darkLightMode() {
//   // Get current theme color through default-colored text
//   var currentMode = document.querySelectorAll(
//     "*:not(.fixed-color, .dynamic-color)"
//   )[0].style.color;

//   // White-to-black
//   if (currentMode == "white") {
//     // Set all default-colored elements to theme color
//     for (const elem of document.querySelectorAll(
//       "*:not(.fixed-color, .dynamic-color)"
//     )) {
//       elem.style.color = "black";
//     }

//     // Set backgrounds to theme color
//     document.body.style.backgroundColor = "black";
//     for (const elem of document.getElementsByClassName("card")) {
//       elem.style.background =
//         "linear-gradient(black 30%, rgba(76, 0, 255, 0.6) 100%)";
//     }

//     // Set all default-colored text to inverse of theme color
//     for (const elem of document.querySelectorAll(
//       "p:not(.fixed-color, .dynamic-color), h1:not(.fixed-color, .dynamic-color), h2:not(.fixed-color, .dynamic-color), h3:not(.fixed-color, .dynamic-color), h4:not(.fixed-color, .dynamic-color), span:not(.fixed-color, .dynamic-color), label:not(.fixed-color, .dynamic-color), div:not(.fixed-color, .dynamic-color)"
//     )) {
//       elem.style.color = "white";
//     }

//     // Set dark-background elements to white (as they are falsely included in the first block)
//     for (const elem of document.getElementsByClassName("grid-sub-score")) {
//       elem.style.color = "white";
//     }

//     // Reconfigure theme toggle
//     document.getElementById("view-mode-flag").innerText = "Light";
//     document.getElementById("view-mode-flag").style.color = "white";
//     document.getElementById("view-mode-toggle").style.backgroundColor = "black";

//     // Black-to-white
//   } else {
//     // Set all default-colored elements to theme color
//     for (const elem of document.querySelectorAll(
//       "*:not(.fixed-color, .dynamic-color)"
//     )) {
//       elem.style.color = "white";
//     }

//     // Set backgrounds to theme color
//     document.body.style.backgroundColor = "white";
//     for (const elem of document.getElementsByClassName("card")) {
//       elem.style.background =
//         "linear-gradient(white 30%, rgba(76, 0, 255, 0.6) 100%)";
//     }

//     // Set all default-colored text to inverse of theme color
//     for (const elem of document.querySelectorAll(
//       "p:not(.fixed-color, .dynamic-color), h1:not(.fixed-color, .dynamic-color), h2:not(.fixed-color, .dynamic-color), h3:not(.fixed-color, .dynamic-color), h4:not(.fixed-color, .dynamic-color), span:not(.fixed-color, .dynamic-color), label:not(.fixed-color, .dynamic-color), div:not(.fixed-color, .dynamic-color)"
//     )) {
//       elem.style.color = "black";
//     }

//     // Set light-background elements to black (as they are falsely included in the first block)
//     document.getElementById("matchup-button").style.color = "black";
//     document.getElementById("reset-button").style.color = "black";
//     document.getElementById("batter-dropdown").style.color = "black";
//     document.getElementById("pitcher-dropdown").style.color = "black";

//     // Reconfigure theme toggle
//     document.getElementById("view-mode-flag").innerText = "Dark";
//     document.getElementById("view-mode-flag").style.color = "black";
//     document.getElementById("view-mode-toggle").style.backgroundColor = "white";
//   }
// }

async function loadPage() {
  loadDropdowns();
  loadSliders(NUM_SLIDERS);
  loadCells();
}
