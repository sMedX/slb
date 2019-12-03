import { AttributeType, IAttributeValue } from '@/models';

export interface IAttributeObject {
    name: string;
    description: string;
    [value: string]: IAttributeValue | string;
}

export interface IAttributesResponse {
    [name: string]: IAttributeObject;
}