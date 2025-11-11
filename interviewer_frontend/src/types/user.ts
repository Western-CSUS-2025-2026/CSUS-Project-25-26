export interface User {
  firstName: string;
  lastName: string;
  email: string;
  creationDate: string;
}
export const defaultUser: User = {
  firstName: "Lucas",
  lastName: "Vanderwielen",
  email: "lvand56@uwo.ca",
  creationDate: "2022-09-27T18:00:00",
};
