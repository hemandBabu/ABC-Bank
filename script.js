const rawInput = document.getElementById("rawInput");
const formattedOutput = document.getElementById("formattedOutput");
const delimiterSelect = document.getElementById("delimiter");
const numberingSelect = document.getElementById("numbering");
const prefixInput = document.getElementById("prefix");
const suffixInput = document.getElementById("suffix");
const trimInput = document.getElementById("trim");
const formatBtn = document.getElementById("formatBtn");
const copyBtn = document.getElementById("copyBtn");
const clearBtn = document.getElementById("clearBtn");
const inputCount = document.getElementById("inputCount");
const outputCount = document.getElementById("outputCount");
const statusText = document.getElementById("statusText");

const romanNumerals = [
  "I",
  "II",
  "III",
  "IV",
  "V",
  "VI",
  "VII",
  "VIII",
  "IX",
  "X",
];

const getDelimiter = () => {
  const value = delimiterSelect.value;
  if (value === "comma") {
    return ",";
  }
  if (value === "semicolon") {
    return ";";
  }
  return "\n";
};

const splitQuestions = (text) => {
  const delimiter = getDelimiter();
  if (!text.trim()) {
    return [];
  }
  return text
    .split(delimiter)
    .map((item) => (trimInput.checked ? item.trim() : item))
    .filter((item) => item.length > 0);
};

const formatNumber = (index) => {
  if (numberingSelect.value === "none") {
    return "";
  }
  if (numberingSelect.value === "roman") {
    return romanNumerals[index] || `${index + 1}`;
  }
  return `${index + 1}`;
};

const buildOutput = () => {
  const questions = splitQuestions(rawInput.value);
  const prefix = prefixInput.value.trim();
  const suffix = suffixInput.value.trim();
  const formatted = questions.map((question, index) => {
    const number = formatNumber(index);
    const numberPart = number ? `${number}. ` : "";
    const prefixPart = prefix ? `${prefix} ` : "";
    const suffixPart = suffix ? ` ${suffix}` : "";
    return `${numberPart}${prefixPart}${question}${suffixPart}`.trim();
  });

  formattedOutput.value = formatted.join("\n");
  outputCount.textContent = `${formatted.length} questions formatted`;
  statusText.textContent = formatted.length
    ? "Formatted and ready to copy."
    : "Waiting for input…";
};

const updateCounts = () => {
  const questions = splitQuestions(rawInput.value);
  inputCount.textContent = `${questions.length} questions detected`;
};

formatBtn.addEventListener("click", () => {
  buildOutput();
});

copyBtn.addEventListener("click", async () => {
  if (!formattedOutput.value.trim()) {
    statusText.textContent = "Nothing to copy yet.";
    return;
  }
  try {
    await navigator.clipboard.writeText(formattedOutput.value);
    statusText.textContent = "Copied formatted questions to clipboard.";
  } catch (error) {
    statusText.textContent = "Clipboard blocked. Copy manually.";
  }
});

clearBtn.addEventListener("click", () => {
  rawInput.value = "";
  formattedOutput.value = "";
  updateCounts();
  outputCount.textContent = "0 questions formatted";
  statusText.textContent = "Waiting for input…";
});

rawInput.addEventListener("input", () => {
  updateCounts();
});

[delimiterSelect, numberingSelect, prefixInput, suffixInput, trimInput].forEach(
  (control) => {
    control.addEventListener("change", () => {
      if (formattedOutput.value.trim()) {
        buildOutput();
      }
    });
  }
);

updateCounts();
