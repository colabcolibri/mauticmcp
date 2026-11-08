export const RESOURCE_NAMES = [
  'contacts',
  'campaigns',
  'emails',
  'segments',
  'forms',
  'companies',
  'categories',
  'pages',
  'assets',
  'focus',
  'points',
  'pointTriggers',
  'pointGroups',
  'stages',
  'tags',
  'reports',
] as const;

export const CREATABLE = [
  'campaigns',
  'emails',
  'segments',
  'forms',
  'companies',
  'categories',
  'pages',
  'assets',
  'focus',
  'points',
  'pointTriggers',
  'pointGroups',
  'stages',
  'tags',
  'reports',
] as const;

export type ResourceName = (typeof RESOURCE_NAMES)[number];
export type CreatableName = (typeof CREATABLE)[number];

export interface ResourceSpec {
  name: ResourceName;
  slug: string;
  collectionKeys: string[];
  itemKeys: string[];
  listFields: string[];
  detailFields: string[];
}

const specs: Record<ResourceName, ResourceSpec> = {
  contacts: {
    name: 'contacts',
    slug: 'contacts',
    collectionKeys: ['contacts'],
    itemKeys: ['contact'],
    listFields: ['id', 'email', 'firstname', 'lastname', 'points'],
    detailFields: ['id', 'email', 'firstname', 'lastname', 'points', 'phone', 'company', 'tags', 'owner', 'stage'],
  },
  campaigns: {
    name: 'campaigns',
    slug: 'campaigns',
    collectionKeys: ['campaigns'],
    itemKeys: ['campaign'],
    listFields: ['id', 'name', 'description', 'isPublished', 'category'],
    detailFields: ['id', 'name', 'description', 'isPublished', 'category', 'events', 'lists', 'forms'],
  },
  emails: {
    name: 'emails',
    slug: 'emails',
    collectionKeys: ['emails'],
    itemKeys: ['email'],
    listFields: ['id', 'name', 'subject', 'emailType', 'isPublished'],
    detailFields: [
      'id',
      'name',
      'subject',
      'emailType',
      'isPublished',
      'fromName',
      'fromAddress',
      'replyToAddress',
      'lists',
      'category',
      'plainText',
      'customHtml',
    ],
  },
  segments: {
    name: 'segments',
    slug: 'segments',
    collectionKeys: ['lists', 'segments'],
    itemKeys: ['list', 'segment'],
    listFields: ['id', 'name', 'alias', 'isPublished'],
    detailFields: ['id', 'name', 'alias', 'isPublished', 'description', 'filters'],
  },
  forms: {
    name: 'forms',
    slug: 'forms',
    collectionKeys: ['forms'],
    itemKeys: ['form'],
    listFields: ['id', 'name', 'isPublished', 'formType'],
    detailFields: ['id', 'name', 'isPublished', 'formType', 'description', 'fields'],
  },
  companies: {
    name: 'companies',
    slug: 'companies',
    collectionKeys: ['companies'],
    itemKeys: ['company'],
    listFields: ['id', 'companyname', 'companyemail', 'companycity'],
    detailFields: ['id', 'companyname', 'companyemail', 'companycity', 'companyphone', 'companywebsite'],
  },
  categories: {
    name: 'categories',
    slug: 'categories',
    collectionKeys: ['categories'],
    itemKeys: ['category'],
    listFields: ['id', 'title', 'alias', 'bundle'],
    detailFields: ['id', 'title', 'alias', 'bundle', 'description', 'isPublished'],
  },
  pages: {
    name: 'pages',
    slug: 'pages',
    collectionKeys: ['pages'],
    itemKeys: ['page'],
    listFields: ['id', 'title', 'alias', 'isPublished'],
    detailFields: ['id', 'title', 'alias', 'isPublished', 'template', 'metaDescription', 'customHtml'],
  },
  assets: {
    name: 'assets',
    slug: 'assets',
    collectionKeys: ['assets'],
    itemKeys: ['asset'],
    listFields: ['id', 'title', 'alias', 'storageLocation', 'isPublished'],
    detailFields: ['id', 'title', 'alias', 'description', 'storageLocation', 'remotePath', 'isPublished', 'category'],
  },
  focus: {
    name: 'focus',
    slug: 'focus',
    collectionKeys: ['focus'],
    itemKeys: ['focus'],
    listFields: ['id', 'name', 'type', 'style', 'isPublished'],
    detailFields: ['id', 'name', 'type', 'style', 'website', 'isPublished', 'category', 'properties'],
  },
  points: {
    name: 'points',
    slug: 'points',
    collectionKeys: ['points'],
    itemKeys: ['point'],
    listFields: ['id', 'name', 'type', 'delta', 'isPublished'],
    detailFields: ['id', 'name', 'type', 'delta', 'description', 'isPublished', 'category'],
  },
  pointTriggers: {
    name: 'pointTriggers',
    slug: 'points/triggers',
    collectionKeys: ['triggers'],
    itemKeys: ['trigger'],
    listFields: ['id', 'name', 'points', 'isPublished'],
    detailFields: ['id', 'name', 'points', 'color', 'description', 'isPublished', 'category'],
  },
  pointGroups: {
    name: 'pointGroups',
    slug: 'points/groups',
    collectionKeys: ['pointGroups'],
    itemKeys: ['pointGroup'],
    listFields: ['id', 'name'],
    detailFields: ['id', 'name', 'description'],
  },
  stages: {
    name: 'stages',
    slug: 'stages',
    collectionKeys: ['stages'],
    itemKeys: ['stage'],
    listFields: ['id', 'name', 'weight', 'isPublished'],
    detailFields: ['id', 'name', 'weight', 'description', 'isPublished', 'category'],
  },
  tags: {
    name: 'tags',
    slug: 'tags',
    collectionKeys: ['tags'],
    itemKeys: ['tag'],
    listFields: ['id', 'tag', 'description'],
    detailFields: ['id', 'tag', 'description'],
  },
  reports: {
    name: 'reports',
    slug: 'reports',
    collectionKeys: ['reports'],
    itemKeys: ['report'],
    listFields: ['id', 'name', 'source', 'description', 'isScheduled'],
    detailFields: ['id', 'name', 'source', 'description', 'isScheduled', 'columns'],
  },
};

export function resourceSpec(name: ResourceName): ResourceSpec {
  return specs[name];
}
