-- Optional: Table definitions for Bank Customer Churn dataset
-- Adapt to your actual DB (e.g. SQLite, PostgreSQL). Column names from Kaggle.

/*
CREATE TABLE bank_churn (
    RowNumber      INT,
    CustomerId     INT,
    Surname        VARCHAR(100),
    CreditScore    INT,
    Geography      VARCHAR(50),
    Gender         VARCHAR(10),
    Age            INT,
    Tenure         INT,
    Balance        FLOAT,
    NumOfProducts  INT,
    HasCrCard      INT,
    IsActiveMember INT,
    EstimatedSalary FLOAT,
    Exited         INT
);

-- Indexes for common filters
CREATE INDEX idx_churn_geography ON bank_churn(Geography);
CREATE INDEX idx_churn_exited ON bank_churn(Exited);
CREATE INDEX idx_churn_tenure ON bank_churn(Tenure);
*/
