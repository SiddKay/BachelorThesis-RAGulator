export const questionsData = [
  {
    id: 1,
    text: "What is the capital of France?",
    important: true,
    answers: [
      { id: 1, questionId: 1, configVersion: 1, text: "Paris", comments: [], score: 0 },
      {
        id: 2,
        questionId: 1,
        configVersion: 2,
        text: "Paris, the City of Light",
        comments: [],
        score: 0
      }
    ]
  },
  {
    id: 2,
    text: "Who wrote 'Romeo and Juliet'?",
    important: false,
    answers: [
      {
        id: 3,
        questionId: 2,
        configVersion: 1,
        text: "William Shakespeare",
        comments: [],
        score: 0
      },
      {
        id: 4,
        questionId: 2,
        configVersion: 2,
        text: "The Bard of Avon, William Shakespeare",
        comments: [],
        score: 0
      }
    ]
  },
  {
    id: 3,
    text: "What is the largest planet in our solar system?",
    important: false,
    answers: [
      { id: 5, questionId: 3, configVersion: 1, text: "Jupiter", comments: [], score: 0 },
      {
        id: 6,
        questionId: 3,
        configVersion: 2,
        text: "Jupiter, the gas giant",
        comments: [],
        score: 0
      }
    ]
  }
];
