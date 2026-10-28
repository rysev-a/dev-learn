-- Quiz of book 13, chapter 6 (English). The structure must match the Russian file.

INSERT INTO quizzes (book_id, chapter, kind, title) VALUES (13, 6, 'theory', 'Quiz: lists');
INSERT INTO quiz_questions (book_id, chapter, ord, q, options, answer, expl) VALUES (13, 6, 0, 'items = ["a", "b", "c"]. What does items[0] return?', '["\"a\"", "\"b\"", "An error", "\"c\""]', 0, 'Counting starts from zero: the first element has index 0.');
INSERT INTO quiz_questions (book_id, chapter, ord, q, options, answer, expl) VALUES (13, 6, 1, 'How do you get the last element of a list without knowing its length?', '["items[0]", "items[-1]", "items[last]", "items.len"]', 1, 'Negative indexes count from the end: -1 is the last, -2 is the second to last.');
INSERT INTO quiz_questions (book_id, chapter, ord, q, options, answer, expl) VALUES (13, 6, 2, 'How do you add an element to the end of a list?', '["items.add(x)", "items.append(x)", "items + x", "push(items, x)"]', 1, 'The append method adds an element to the end, so the list grows on the fly.');
INSERT INTO quiz_questions (book_id, chapter, ord, q, options, answer, expl) VALUES (13, 6, 3, 'What does len([10, 20, 30]) return?', '["2", "3", "30", "60"]', 1, 'len returns the number of elements, here three.');
INSERT INTO quiz_questions (book_id, chapter, ord, q, options, answer, expl) VALUES (13, 6, 4, 'What does the slice [1, 2, 3, 4][1:3] return?', '["[1, 2]", "[2, 3]", "[2, 3, 4]", "[1, 2, 3]"]', 1, 'A slice takes from index 1 inclusive up to 3 exclusive, the same logic as range.');
