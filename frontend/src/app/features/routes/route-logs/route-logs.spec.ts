import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RouteLogs } from './route-logs';

describe('RouteLogs', () => {
  let component: RouteLogs;
  let fixture: ComponentFixture<RouteLogs>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouteLogs],
    }).compileComponents();

    fixture = TestBed.createComponent(RouteLogs);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
