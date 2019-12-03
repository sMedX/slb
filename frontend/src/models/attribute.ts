export enum AttributeType {
    LIST = 'string',
    NUMBER = 'float64'
}

interface IAttributeList {
    type: AttributeType.LIST;
    values: Array<string>;
}

interface IAttributeNumber {
    name: string;
    type: AttributeType.NUMBER;
    min: number;
    max: number;
}

export type IAttributeValue = IAttributeList | IAttributeNumber;

export interface IAttribute {
    name: string;
    displayName: string;
    description: string;
    values: Array<IAttributeValue>;
}